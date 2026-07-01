from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from core.forms import SearchForm, TeacherFilterForm, TeacherForm
from core.models import Direction, Teacher
from core.services.teacher_stats import (
    get_teacher_attendance_log,
    get_teacher_extras,
    get_teacher_report,
    get_teacher_students_by_direction,
)


def _build_filter_params(request, tab=None, exclude=None):
    params = request.GET.copy()
    if tab:
        params['tab'] = tab
    for key in exclude or ('edit',):
        params.pop(key, None)
    return params.urlencode()


def _teacher_direction_ids_set(teacher):
    ids = set(teacher.directions.values_list('id', flat=True))
    for did in teacher.schedule_slots.filter(is_archived=False).values_list('direction_id', flat=True):
        ids.add(did)
    return ids


@login_required
def teacher_list(request):
    search_form = SearchForm(request.GET or None)
    teachers = Teacher.objects.prefetch_related('directions').annotate(
        slots_count=Count('schedule_slots', filter=Q(schedule_slots__is_archived=False)),
    ).order_by('name')

    if search_form.is_valid():
        q = search_form.cleaned_data.get('q', '').strip()
        if q:
            teachers = teachers.filter(
                Q(name__icontains=q)
                | Q(phone__icontains=q)
                | Q(email__icontains=q)
                | Q(notes__icontains=q)
            )
        direction = search_form.cleaned_data.get('direction')
        if direction:
            teachers = teachers.filter(directions=direction).distinct()

    return render(request, 'pages/teachers/list.html', {
        'teachers': teachers,
        'search_form': search_form,
        'page_title': 'Преподаватели',
        'total_count': teachers.count(),
    })


@login_required
def teacher_create(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save()
            messages.success(request, f'Преподаватель «{teacher.name}» добавлен.')
            return redirect('core:teacher_detail', pk=teacher.pk)
    else:
        form = TeacherForm()

    return render(request, 'pages/teachers/form.html', {
        'form': form,
        'page_title': 'Новый преподаватель',
        'is_create': True,
    })


@login_required
def teacher_detail(request, pk):
    teacher = get_object_or_404(
        Teacher.objects.prefetch_related('directions', 'schedule_slots__direction'),
        pk=pk,
    )

    today = timezone.localdate()
    get_data = request.GET.copy() if request.GET else {}
    if 'date_from' not in get_data:
        get_data['date_from'] = today.replace(day=1).isoformat()
    if 'date_to' not in get_data:
        get_data['date_to'] = today.isoformat()

    teacher_directions = Direction.objects.filter(
        id__in=_teacher_direction_ids_set(teacher),
    ).order_by('name')

    filter_form = TeacherFilterForm(get_data, teacher_directions=teacher_directions)
    date_from = date_to = None
    direction_ids = None
    if filter_form.is_valid():
        date_from = filter_form.cleaned_data.get('date_from')
        date_to = filter_form.cleaned_data.get('date_to')
        selected = filter_form.cleaned_data.get('directions')
        if selected:
            direction_ids = [d.pk for d in selected]

    report = get_teacher_report(teacher, date_from, date_to, direction_ids)
    attendance_log = get_teacher_attendance_log(teacher, date_from, date_to, direction_ids)
    extras = get_teacher_extras(teacher, date_from, date_to, direction_ids)
    students_by_direction = get_teacher_students_by_direction(teacher)

    active_tab = request.GET.get('tab', 'salary')
    if active_tab not in ('salary', 'attendance', 'extras', 'directions'):
        active_tab = 'salary'

    edit_mode = request.GET.get('edit') == '1'
    if request.method == 'POST' and request.POST.get('action') == 'save_teacher':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные преподавателя сохранены.')
            return redirect('core:teacher_detail', pk=pk)
        messages.error(request, 'Проверьте поля формы.')
    else:
        form = TeacherForm(instance=teacher) if edit_mode else None

    assigned_ids = set(teacher.directions.values_list('id', flat=True))
    available_directions = Direction.objects.exclude(id__in=assigned_ids).order_by('name')

    filter_params = _build_filter_params(request, tab=None, exclude=('edit', 'tab'))
    filter_suffix = f'&{filter_params}' if filter_params else ''

    return render(request, 'pages/teachers/detail.html', {
        'teacher': teacher,
        'form': form,
        'edit_mode': edit_mode,
        'filter_form': filter_form,
        'teacher_directions': teacher_directions,
        'filter_params': filter_params,
        'filter_suffix': filter_suffix,
        'report': report,
        'attendance_log': attendance_log,
        'extras': extras,
        'students_by_direction': students_by_direction,
        'available_directions': available_directions,
        'active_tab': active_tab,
        'page_title': teacher.name,
    })


@login_required
@require_POST
def teacher_assign_direction(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    direction = get_object_or_404(Direction, pk=request.POST.get('direction_id'))
    teacher.directions.add(direction)
    messages.success(request, f'Направление «{direction.name}» добавлено.')
    tab = request.POST.get('tab', 'directions')
    return redirect(f"{reverse('core:teacher_detail', kwargs={'pk': pk})}?tab={tab}")


@login_required
@require_POST
def teacher_remove_direction(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    direction = get_object_or_404(Direction, pk=request.POST.get('direction_id'))
    teacher.directions.remove(direction)
    messages.success(request, f'Направление «{direction.name}» убрано.')
    tab = request.POST.get('tab', 'directions')
    return redirect(f"{reverse('core:teacher_detail', kwargs={'pk': pk})}?tab={tab}")


@login_required
@require_POST
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    name = teacher.name
    teacher.delete()
    messages.success(request, f'Преподаватель «{name}» удалён.')
    return redirect('core:teacher_list')
