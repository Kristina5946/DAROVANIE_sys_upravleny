from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from accounts.permissions import user_can_view_finance
from core.decorators import admin_required
from core.forms import PaymentFilterForm, PaymentQuickAddForm
from core.models import Direction, Payment, PaymentType, Student
from core.services.payments_report import (
    export_payments_excel,
    get_filtered_payments,
    get_payments_charts,
    get_payments_summary,
)


def _filter_params(request, exclude_edit=False):
    params = request.GET.copy()
    if exclude_edit:
        params.pop('edit', None)
    return params


def _build_filter_data(request):
    today = timezone.localdate()
    get_data = request.GET.copy() if request.GET else {}
    if 'date_from' not in get_data:
        get_data['date_from'] = today.replace(day=1).isoformat()
    if 'date_to' not in get_data:
        get_data['date_to'] = today.isoformat()
    return get_data


def _payments_from_filters(filter_form):
    date_from = date_to = direction = payment_type = q = None
    if filter_form.is_valid():
        date_from = filter_form.cleaned_data.get('date_from')
        date_to = filter_form.cleaned_data.get('date_to')
        direction = filter_form.cleaned_data.get('direction')
        payment_type = filter_form.cleaned_data.get('payment_type')
        q = filter_form.cleaned_data.get('q', '')
    return get_filtered_payments(
        date_from=date_from,
        date_to=date_to,
        direction_id=direction.pk if direction else None,
        payment_type=payment_type or None,
        q=q,
    )


@login_required
def payments_report(request):
    get_data = _build_filter_data(request)
    filter_form = PaymentFilterForm(get_data)
    payments_qs = _payments_from_filters(filter_form)
    edit_mode = request.GET.get('edit') == '1'
    show_finance_stats = user_can_view_finance(request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_payment':
            add_form = PaymentQuickAddForm(request.POST)
            if add_form.is_valid():
                payment = add_form.save(commit=False)
                payment.created_by = request.user
                payment.save()
                messages.success(request, 'Оплата добавлена.')
            else:
                messages.error(request, 'Проверьте форму добавления оплаты.')
        elif action == 'save_payments':
            updated = 0
            for key, value in request.POST.items():
                if not key.startswith('payment_amount_'):
                    continue
                pay_id = key.replace('payment_amount_', '')
                try:
                    payment = Payment.objects.get(pk=pay_id)
                except (Payment.DoesNotExist, ValueError):
                    continue
                if request.POST.get(f'payment_delete_{pay_id}'):
                    payment.delete()
                    updated += 1
                    continue
                try:
                    payment.amount = Decimal(str(value).replace(',', '.'))
                except (InvalidOperation, ValueError):
                    pass
                payment.notes = request.POST.get(f'payment_notes_{pay_id}', payment.notes)
                date_str = request.POST.get(f'payment_date_{pay_id}')
                if date_str:
                    payment.payment_date = date_str
                ptype = request.POST.get(f'payment_type_{pay_id}')
                if ptype:
                    payment.payment_type = ptype
                direction_id = request.POST.get(f'payment_direction_{pay_id}')
                if direction_id:
                    payment.direction_id = direction_id
                payment.save()
                updated += 1
            messages.success(request, f'Сохранено записей: {updated}.')
        qs = _filter_params(request)
        return redirect(f"{reverse('core:payments_report')}?{qs.urlencode()}")

    summary = get_payments_summary(payments_qs) if show_finance_stats else None
    charts = get_payments_charts(payments_qs) if show_finance_stats else None
    add_form = PaymentQuickAddForm()
    directions = Direction.objects.order_by('name')
    export_qs = _filter_params(request, exclude_edit=True).urlencode()

    return render(request, 'pages/payments_report.html', {
        'filter_form': filter_form,
        'payments': payments_qs,
        'summary': summary,
        'charts': charts,
        'add_form': add_form,
        'directions': directions,
        'payment_types': PaymentType.choices,
        'edit_mode': edit_mode,
        'show_finance_stats': show_finance_stats,
        'export_qs': export_qs,
        'page_title': 'Оплаты',
    })


@admin_required
@require_GET
def payments_export(request):
    get_data = _build_filter_data(request)
    filter_form = PaymentFilterForm(get_data)
    payments_qs = _payments_from_filters(filter_form)
    content = export_payments_excel(payments_qs)
    date_from = filter_form.cleaned_data.get('date_from') if filter_form.is_valid() else ''
    date_to = filter_form.cleaned_data.get('date_to') if filter_form.is_valid() else ''
    filename = f'payments_{date_from}_{date_to}.xlsx'
    response = HttpResponse(
        content,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
