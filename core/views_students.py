from datetime import date
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from core.forms import PaymentForm, SearchForm, StudentForm, SubscriptionTopUpForm
from core.models import AttendanceRecord, Direction, Payment, PaymentType, Student
from core.services.subscriptions import (
    create_custom_subscription,
    estimate_amount_for_lessons,
    get_direction_card,
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
                        record.save()
                    except AttendanceRecord.DoesNotExist:
                        pass
            messages.success(request, 'Посещения обновлены.')
            return redirect(reverse('core:student_detail', kwargs={'pk': pk}) + '?tab=attendance')

    if edit_mode and form is None:
        form = StudentForm(instance=student)
    direction_cards = [get_direction_card(student, d) for d in student.directions.all()]
    payments = student.payments.select_related('direction').order_by('-payment_date')[:50]
    attendance = (
        student.attendance.select_related('direction', 'schedule_slot', 'subscription')
        .order_by('-lesson_date')[:50]
    )

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
    try:
        direction = Direction.objects.get(pk=direction_id)
        lessons_count = max(1, int(lessons))
    except (Direction.DoesNotExist, ValueError):
        return JsonResponse({'error': 'Неверные параметры'}, status=400)

    amount = estimate_amount_for_lessons(direction, lessons_count)
    lessons_in_month = direction.subscription_cost and lessons_count
    return JsonResponse({
        'amount': str(amount),
        'lessons_in_month': lessons_count,
        'subscription_cost': str(direction.subscription_cost),
    })
