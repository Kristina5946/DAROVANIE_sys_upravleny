from datetime import date, timedelta
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from core.forms import PaymentForm, SearchForm, StudentForm, SubscriptionEditForm, SubscriptionTopUpForm
from core.models import AttendanceRecord, Direction, Payment, PaymentType, Student, Subscription, Teacher
from core.services.schedule_day import assign_attendance_teacher
from core.services.subscriptions import (
    calculate_subscription_end_date,
    create_custom_subscription,
    estimate_amount_for_lessons,
    get_direction_card,
    link_attendance_to_active_subscription,
    resolve_subscription_period,
    sync_subscription_from_payment,
    update_subscription,
)


def _student_queryset():
    return Student.objects.select_related('parent').prefetch_related('directions')


def _apply_student_filters(qs, form):
    if not form.is_valid():
        return qs
    q = form.cleaned_data.get('q', '').strip()
    if q:
        qs = qs.filter(
            Q(name__icontains=q)
            | Q(parent__name__icontains=q)
            | Q(parent__phone__icontains=q)
            | Q(notes__icontains=q)
        )
    direction = form.cleaned_data.get('direction')
    if direction:
        qs = qs.filter(directions=direction)
    gender = form.cleaned_data.get('gender')
    if gender:
        qs = qs.filter(gender=gender)
    return qs.distinct()


def _attendance_filter_params(request):
    params = request.GET.copy()
    for key in ('tab', 'edit_attendance', 'attendance_page'):
        params.pop(key, None)
    return params.urlencode()


def _attendance_query_params(request, **updates):
    params = request.GET.copy()
    params['tab'] = 'attendance'
    params.pop('edit_attendance', None)
    params.pop('attendance_page', None)
    for key, value in updates.items():
        params[key] = value
    return params.urlencode()


@login_required
def student_list(request):
    form = SearchForm(request.GET or None)
    students = _apply_student_filters(_student_queryset(), form).order_by('name')

  # Сохраняем фильтры в query string для ссылок
    filter_qs = request.GET.urlencode()

    return render(request, 'pages/students/list.html', {
        'students': students,
        'search_form': form,
        'filter_qs': filter_qs,
        'page_title': 'Ученики',
        'total_count': students.count(),
    })


@login_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Ученик «{student.name}» добавлен.')
            return redirect('core:student_detail', pk=student.pk)
    else:
        form = StudentForm()

    return render(request, 'pages/students/form.html', {
        'form': form,
        'page_title': 'Новый ученик',
        'is_create': True,
    })


@login_required
def student_detail(request, pk):
    student = get_object_or_404(
        _student_queryset(),
        pk=pk,
    )
    edit_mode = request.GET.get('edit') == '1'
    edit_payments = request.GET.get('edit_payments') == '1'
    edit_attendance = request.GET.get('edit_attendance') == '1'
    active_tab = request.GET.get('tab', 'payments')
    form = None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'save_profile':
            form = StudentForm(request.POST, instance=student)
            if form.is_valid():
                form.save()
                messages.success(request, 'Данные ученика сохранены.')
                return redirect('core:student_detail', pk=pk)
            messages.error(request, 'Не удалось сохранить. Проверьте поля формы.')
            edit_mode = True
        elif action == 'top_up':
            topup_form = SubscriptionTopUpForm(student, request.POST)
            if topup_form.is_valid():
                direction = topup_form.cleaned_data['direction']
                create_custom_subscription(
                    student=student,
                    direction=direction,
                    payment_date=topup_form.cleaned_data['payment_date'],
                    amount=topup_form.cleaned_data['amount'],
                    total_lessons=topup_form.cleaned_data['lessons_count'],
                    notes=topup_form.cleaned_data.get('notes') or '',
                    created_by=request.user,
                    from_month_start=topup_form.cleaned_data.get('from_month_start', True),
                    from_next_month=topup_form.cleaned_data.get('from_next_month', False),
                    end_date=topup_form.cleaned_data.get('end_date'),
                )
                messages.success(
                    request,
                    f'Абонемент по «{direction.name}» оформлен: '
                    f'{topup_form.cleaned_data["lessons_count"]} занятий, '
                    f'{topup_form.cleaned_data["amount"]} ₽.',
                )
                return redirect('core:student_detail', pk=pk)
            else:
                messages.error(request, 'Проверьте данные абонемента.')
        elif action == 'edit_subscription':
            subscription = get_object_or_404(
                Subscription.objects.select_related('direction', 'payment'),
                pk=request.POST.get('subscription_id'),
                student=student,
            )
            edit_form = SubscriptionEditForm(request.POST, instance=subscription)
            if edit_form.is_valid():
                try:
                    update_subscription(
                        subscription,
                        total_lessons=edit_form.cleaned_data['total_lessons'],
                        carried_lessons=edit_form.cleaned_data['carried_lessons'],
                        amount=edit_form.cleaned_data['amount'],
                        start_date=edit_form.cleaned_data['start_date'],
                        end_date=edit_form.cleaned_data['end_date'],
                        payment_date=edit_form.cleaned_data['payment_date'],
                        notes=edit_form.cleaned_data.get('notes') or '',
                        auto_end_date=edit_form.cleaned_data.get('auto_end_date', False),
                    )
                    messages.success(request, f'Абонемент «{subscription.direction.name}» обновлён.')
                except ValueError as exc:
                    messages.error(request, str(exc))
            else:
                messages.error(request, 'Проверьте данные абонемента.')
            return redirect('core:student_detail', pk=pk)
        elif action == 'add_payment':
            payment_form = PaymentForm(request.POST)
            payment_form.instance.student = student
            if payment_form.is_valid():
                payment = payment_form.save(commit=False)
                payment.student = student
                payment.created_by = request.user
                payment.save()
                messages.success(request, 'Оплата добавлена.')
                return redirect(reverse('core:student_detail', kwargs={'pk': pk}) + '?tab=payments')
        elif action == 'save_payments':
            for key, value in request.POST.items():
                if key.startswith('payment_amount_'):
                    pay_id = key.replace('payment_amount_', '')
                    try:
                        payment = Payment.objects.get(pk=pay_id, student=student)
                        payment.amount = Decimal(value)
                        payment.notes = request.POST.get(f'payment_notes_{pay_id}', payment.notes)
                        date_str = request.POST.get(f'payment_date_{pay_id}')
                        if date_str:
                            payment.payment_date = date_str
                        ptype = request.POST.get(f'payment_type_{pay_id}')
                        if ptype:
                            payment.payment_type = ptype
                        if request.POST.get(f'payment_delete_{pay_id}'):
                            payment.delete()
                        else:
                            payment.save()
                            sync_subscription_from_payment(payment)
                    except (Payment.DoesNotExist, InvalidOperation):
                        pass
            messages.success(request, 'Оплаты обновлены.')
            return redirect(reverse('core:student_detail', kwargs={'pk': pk}) + '?tab=payments')
        elif action == 'save_attendance':
            for key, value in request.POST.items():
                if key.startswith('att_present_'):
                    att_id = key.replace('att_present_', '')
                    try:
                        record = AttendanceRecord.objects.get(pk=att_id, student=student)
                        record.present = f'att_present_{att_id}' in request.POST
                        record.paid = f'att_paid_{att_id}' in request.POST
                        record.note = request.POST.get(f'att_note_{att_id}', record.note)
                        record.save(update_fields=['present', 'paid', 'note', 'updated_at'])
                        teacher_id = request.POST.get(f'att_teacher_{att_id}')
                        if str(record.teacher_id or '') != teacher_id:
                            teacher = Teacher.objects.filter(pk=teacher_id).first() if teacher_id else None
                            assign_attendance_teacher(record, teacher)
                        link_attendance_to_active_subscription(record)
                    except (AttendanceRecord.DoesNotExist, ValueError) as exc:
                        if isinstance(exc, ValueError):
                            messages.error(request, exc)
                        pass
            messages.success(request, 'Посещения обновлены.')
            filter_params = _attendance_filter_params(request)
            suffix = f'&{filter_params}' if filter_params else ''
            return redirect(reverse('core:student_detail', kwargs={'pk': pk}) + f'?tab=attendance{suffix}')

    if edit_mode and form is None:
        form = StudentForm(instance=student)
    direction_cards = [get_direction_card(student, d) for d in student.directions.all()]
    payments = student.payments.select_related('direction').order_by('-payment_date')[:50]
    attendance = student.attendance.select_related(
        'direction', 'schedule_slot', 'subscription', 'teacher', 'single_lesson',
    ).order_by('-lesson_date', '-updated_at')
    today = timezone.localdate()
    current_month_start = today.replace(day=1)
    next_month_start = (current_month_start + timedelta(days=32)).replace(day=1)
    current_month_end = next_month_start - timedelta(days=1)
    attendance_date_from = request.GET.get('attendance_date_from', current_month_start.isoformat())
    attendance_date_to = request.GET.get('attendance_date_to', current_month_end.isoformat())
    attendance_direction = request.GET.get('attendance_direction', '')
    attendance_teacher = request.GET.get('attendance_teacher', '')
    attendance_present = request.GET.get('attendance_present', '')
    attendance_paid = request.GET.get('attendance_paid', '')
    attendance_note = request.GET.get('attendance_note', '').strip()
    try:
        date_from = date.fromisoformat(attendance_date_from) if attendance_date_from else None
        date_to = date.fromisoformat(attendance_date_to) if attendance_date_to else None
        if date_from:
            attendance = attendance.filter(lesson_date__gte=date_from)
        if date_to:
            attendance = attendance.filter(lesson_date__lte=date_to)
    except ValueError:
        messages.error(request, 'Укажите дату в формате ГГГГ-ММ-ДД.')
        date_from = current_month_start
        date_to = current_month_end
        attendance_date_from = date_from.isoformat()
        attendance_date_to = date_to.isoformat()
        attendance = attendance.filter(lesson_date__range=(date_from, date_to))
    if attendance_direction:
        attendance = attendance.filter(direction_id=attendance_direction)
    if attendance_teacher:
        attendance = attendance.filter(teacher_id=attendance_teacher)
    if attendance_present in ('0', '1'):
        attendance = attendance.filter(present=attendance_present == '1')
    if attendance_paid in ('0', '1'):
        attendance = attendance.filter(paid=attendance_paid == '1')
    if attendance_note:
        attendance = attendance.filter(note__icontains=attendance_note)
    attendance = Paginator(attendance, 30).get_page(request.GET.get('attendance_page'))

    period_month = date_from.replace(day=1) if date_from else current_month_start
    previous_month = period_month - timedelta(days=1)
    next_month = period_month + timedelta(days=32)
    previous_month_start = previous_month.replace(day=1)
    previous_month_end = (previous_month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    next_month_start = next_month.replace(day=1)
    next_month_end = (next_month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    return render(request, 'pages/students/detail.html', {
        'student': student,
        'form': form,
        'edit_mode': edit_mode,
        'edit_payments': edit_payments,
        'edit_attendance': edit_attendance,
        'active_tab': active_tab,
        'direction_cards': direction_cards,
        'payments': payments,
        'attendance': attendance,
        'attendance_filter_params': _attendance_filter_params(request),
        'attendance_date_from': attendance_date_from,
        'attendance_date_to': attendance_date_to,
        'attendance_previous_month_params': _attendance_query_params(
            request,
            attendance_date_from=previous_month_start.isoformat(),
            attendance_date_to=previous_month_end.isoformat(),
        ),
        'attendance_next_month_params': _attendance_query_params(
            request,
            attendance_date_from=next_month_start.isoformat(),
            attendance_date_to=next_month_end.isoformat(),
        ),
        'attendance_page_params': _attendance_query_params(request),
        'attendance_directions': Direction.objects.filter(attendancerecord__student=student).distinct().order_by('name'),
        'attendance_teachers': Teacher.objects.filter(attendance_snapshots__student=student).distinct().order_by('name'),
        'all_teachers': Teacher.objects.order_by('name'),
        'payment_types': PaymentType.choices,
        'all_directions': Direction.objects.exclude(pk__in=student.directions.values_list('pk', flat=True)),
        'page_title': student.name,
    })


@login_required
@require_POST
def student_assign_direction(request, pk):
    student = get_object_or_404(Student, pk=pk)
    direction_id = request.POST.get('direction_id')
    if direction_id:
        direction = get_object_or_404(Direction, pk=direction_id)
        student.directions.add(direction)
        messages.success(request, f'Направление «{direction.name}» добавлено.')
    return redirect('core:student_detail', pk=pk)


@login_required
@require_GET
def estimate_subscription_api(request):
    direction_id = request.GET.get('direction_id')
    lessons = request.GET.get('lessons', '8')
    student_id = request.GET.get('student_id')
    payment_date_str = request.GET.get('payment_date')
    from_month_start = request.GET.get('from_month_start', '1') != '0'
    from_next_month = request.GET.get('from_next_month', '0') == '1'
    try:
        direction = Direction.objects.get(pk=direction_id)
        lessons_count = max(1, int(lessons))
    except (Direction.DoesNotExist, ValueError):
        return JsonResponse({'error': 'Неверные параметры'}, status=400)

    if payment_date_str:
        try:
            payment_date = date.fromisoformat(payment_date_str)
        except ValueError:
            payment_date = date.today()
    else:
        payment_date = date.today()

    start_date, _ = resolve_subscription_period(
        payment_date, from_month_start, from_next_month=from_next_month,
    )
    end_date = calculate_subscription_end_date(
        direction.id,
        start_date,
        lessons_count,
        student_id=student_id,
    )
    amount = estimate_amount_for_lessons(direction, lessons_count, payment_date)
    return JsonResponse({
        'amount': str(amount),
        'end_date': end_date.isoformat(),
        'start_date': start_date.isoformat(),
        'lessons_in_month': lessons_count,
        'subscription_cost': str(direction.subscription_cost),
    })
