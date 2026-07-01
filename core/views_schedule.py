import json
from datetime import datetime
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from core.forms import ScheduleExceptionForm, ScheduleSlotForm, SearchForm, SingleLessonForm
from core.models import (
    AttendanceRecord,
    Classroom,
    Direction,
    LessonExceptionType,
    LessonType,
    ScheduleException,
    ScheduleSlot,
    Student,
    Teacher,
    WeekDay,
)
from core.services.schedule_day import (
    add_single_or_makeup,
    get_attendance_for_lesson,
    get_lessons_for_date,
    get_week_grid,
    save_lesson_attendance,
)


def _parse_date(value):
    if not value:
        return timezone.localdate()
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return timezone.localdate()


def _cleanup_slot_attendance(slot: ScheduleSlot) -> None:
    """Удаляет лишние записи посещений при смене ученика на индивидуальном слоте."""
    if slot.direction.lesson_type != LessonType.INDIVIDUAL:
        return
    if slot.student_id:
        AttendanceRecord.objects.filter(schedule_slot=slot).exclude(
            student_id=slot.student_id,
        ).delete()


@login_required
def schedule_page(request):
    view = request.GET.get('view', 'today')
    lesson_date = _parse_date(request.GET.get('date'))
    edit_mode = request.GET.get('edit') == '1' and view in ('week', 'table')

    lessons_today = get_lessons_for_date(lesson_date)
    lessons_with_attendance = []
    for lesson in lessons_today:
        if lesson.is_cancelled:
            att = {}
        else:
            att = get_attendance_for_lesson(lesson, lesson_date)
        student_rows = [
            {'student': s, 'record': att.get(s.id)}
            for s in lesson.students
        ]
        lessons_with_attendance.append({
            'lesson': lesson,
            'student_rows': student_rows,
        })

    week_grid = get_week_grid()
    week_days = [
        {'index': i, 'label': label, 'slots': week_grid[i]}
        for i, label in WeekDay.choices
    ]

    search_form = SearchForm(request.GET or None)
    slots_qs = ScheduleSlot.objects.filter(is_archived=False).select_related(
        'direction', 'teacher', 'classroom', 'student',
    ).order_by('day_of_week', 'sort_order', 'start_time')

    if search_form.is_valid():
        q = search_form.cleaned_data.get('q', '').strip()
        if q:
            slots_qs = slots_qs.filter(
                Q(direction__name__icontains=q)
                | Q(teacher__name__icontains=q)
                | Q(classroom__name__icontains=q)
                | Q(student__name__icontains=q)
            )
        direction = search_form.cleaned_data.get('direction')
        if direction:
            slots_qs = slots_qs.filter(direction=direction)

    teacher_filter = request.GET.get('teacher')
    if teacher_filter:
        slots_qs = slots_qs.filter(teacher_id=teacher_filter)

    day_filter = request.GET.get('day')
    if day_filter != '' and day_filter is not None:
        try:
            slots_qs = slots_qs.filter(day_of_week=int(day_filter))
        except ValueError:
            pass

    slot_form = ScheduleSlotForm()
    single_form = SingleLessonForm(initial={'lesson_date': lesson_date})
    exception_form = ScheduleExceptionForm(initial={'lesson_date': lesson_date})

    direction_types = {
        str(d.pk): d.lesson_type for d in Direction.objects.all()
    }
    edit_params = request.GET.copy()
    edit_params['view'] = view
    edit_params['edit'] = '0' if edit_mode else '1'

    return render(request, 'pages/schedule/index.html', {
        'view': view,
        'lesson_date': lesson_date,
        'edit_mode': edit_mode,
        'lessons_with_attendance': lessons_with_attendance,
        'week_days': week_days,
        'table_slots': slots_qs,
        'search_form': search_form,
        'slot_form': slot_form,
        'single_form': single_form,
        'exception_form': exception_form,
        'teachers': Teacher.objects.order_by('name'),
        'directions': Direction.objects.order_by('name'),
        'classrooms': Classroom.objects.order_by('name'),
        'weekday_choices': WeekDay.choices,
        'direction_types_json': json.dumps(direction_types),
        'edit_toggle_url': '?' + edit_params.urlencode(),
        'page_title': 'Расписание',
    })


@login_required
@require_GET
def schedule_direction_students(request):
    direction_id = request.GET.get('direction')
    if not direction_id:
        return JsonResponse({'students': []})
    students = Student.objects.filter(directions__pk=direction_id).order_by('name').distinct()
    return JsonResponse({
        'students': [{'id': str(s.pk), 'name': s.name} for s in students],
    })


@login_required
@require_POST
def schedule_save_attendance(request):
    lesson_date = _parse_date(request.POST.get('lesson_date'))
    lesson_key = request.POST.get('lesson_key', '')
    lessons = {l.key: l for l in get_lessons_for_date(lesson_date)}
    lesson = lessons.get(lesson_key)
    if not lesson or lesson.is_cancelled:
        messages.error(request, 'Занятие не найдено или отменено.')
        return redirect(f'{request.META.get("HTTP_REFERER", "/schedule/")}')

    student_ids = request.POST.getlist('student_id')
    rows = []
    for sid in student_ids:
        rows.append({
            'student_id': sid,
            'present': request.POST.get(f'present_{sid}') == 'on',
            'paid': request.POST.get(f'paid_{sid}') == 'on',
            'note': request.POST.get(f'note_{sid}', ''),
        })
    save_lesson_attendance(lesson, lesson_date, rows)
    messages.success(request, 'Посещения сохранены.')
    return redirect(f'{reverse("core:schedule")}?view=today&date={lesson_date.isoformat()}')


@login_required
@require_POST
def schedule_slot_save(request):
    slot_id = request.POST.get('slot_id')
    instance = get_object_or_404(ScheduleSlot, pk=slot_id) if slot_id else None
    form = ScheduleSlotForm(request.POST, instance=instance)
    if form.is_valid():
        slot = form.save()
        if slot.direction.lesson_type == LessonType.GROUP:
            ScheduleSlot.objects.filter(pk=slot.pk).update(student=None)
            slot.student = None
        _cleanup_slot_attendance(slot)
        if not slot_id:
            max_order = ScheduleSlot.objects.filter(
                day_of_week=slot.day_of_week,
            ).order_by('-sort_order').values_list('sort_order', flat=True).first() or 0
            slot.sort_order = max_order + 1
            slot.save(update_fields=['sort_order'])
        messages.success(request, 'Слот расписания сохранён.')
    else:
        for field, errors in form.errors.items():
            label = form.fields[field].label if field in form.fields else field
            for err in errors:
                messages.error(request, f'{label}: {err}')
    return redirect(request.META.get('HTTP_REFERER', '/schedule/?view=week'))


@login_required
@require_POST
def schedule_slot_duplicate(request, pk):
    slot = get_object_or_404(ScheduleSlot, pk=pk)
    new_slot = ScheduleSlot.objects.get(pk=slot.pk)
    new_slot.pk = None
    new_slot.sort_order = slot.sort_order + 1
    new_slot.save()
    messages.success(request, 'Слот продублирован.')
    return redirect(request.META.get('HTTP_REFERER', '/schedule/?view=week&edit=1'))


@login_required
@require_POST
def schedule_slot_delete(request, pk):
    slot = get_object_or_404(ScheduleSlot, pk=pk)
    slot.delete()
    messages.success(request, 'Слот удалён.')
    return redirect(request.META.get('HTTP_REFERER', '/schedule/?view=week'))


@login_required
@require_POST
def schedule_reorder(request):
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'error': 'invalid json'}, status=400)

    with transaction.atomic():
        for item in payload.get('items', []):
            updates = {'sort_order': item.get('sort_order', 0)}
            if 'day' in item:
                updates['day_of_week'] = item['day']
            ScheduleSlot.objects.filter(pk=item['id']).update(**updates)
    return JsonResponse({'ok': True})


@login_required
@require_POST
def schedule_add_single(request):
    form = SingleLessonForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        amount = data.get('payment_amount')
        if not amount and data['lesson_type'] == 'single':
            amount = data['direction'].single_lesson_cost
        add_single_or_makeup(
            student=data['student'],
            direction=data['direction'],
            teacher=data['teacher'],
            lesson_date=data['lesson_date'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            lesson_type=data['lesson_type'],
            create_payment=data.get('create_payment', False),
            payment_amount=amount,
            notes=data.get('notes', ''),
            created_by=request.user,
        )
        messages.success(request, 'Разовое занятие / отработка добавлено.')
        return redirect(f'{reverse("core:schedule")}?view=today&date={data["lesson_date"].isoformat()}')
    messages.error(request, 'Проверьте форму разового занятия.')
    return redirect(request.META.get('HTTP_REFERER', '/schedule/'))


@login_required
@require_POST
def schedule_add_exception(request):
    form = ScheduleExceptionForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        ScheduleException.objects.update_or_create(
            lesson_date=data['lesson_date'],
            schedule_slot=data['schedule_slot'],
            defaults={
                'exception_type': data['exception_type'],
                'substitute_teacher': data.get('substitute_teacher'),
                'notes': data.get('notes', ''),
            },
        )
        label = 'Замена' if data['exception_type'] == LessonExceptionType.SUBSTITUTION else 'Отмена'
        messages.success(request, f'{label} сохранена.')
        return redirect(f'{reverse("core:schedule")}?view=today&date={data["lesson_date"].isoformat()}')
    messages.error(request, 'Проверьте форму исключения.')
    return redirect(request.META.get('HTTP_REFERER', '/schedule/'))
