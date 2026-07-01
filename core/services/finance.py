"""
Финансовые отчёты: оплаты по направлениям, зарплата, прибыль.
"""
from collections import defaultdict
from datetime import date
from decimal import Decimal

from django.db.models import Sum

from core.models import (
    MaterialPurchase,
    Payment,
    Teacher,
)
from core.services.schedule import month_bounds


def monthly_payments_by_direction(year: int, month: int) -> list[dict]:
    """
    Список оплат по направлениям за месяц.
    Пример: Английский — Есения 4400, Давид 4400.
    """
    start, end = month_bounds(year, month)
    payments = (
        Payment.objects.filter(payment_date__gte=start, payment_date__lte=end, amount__gt=0)
        .select_related('student', 'direction')
        .order_by('direction__name', 'student__name')
    )

    by_direction: dict[str, list] = defaultdict(list)
    for p in payments:
        by_direction[p.direction.name].append({
            'student': p.student.name,
            'student_id': p.student_id,
            'direction_id': p.direction_id,
            'amount': p.amount,
            'type': p.get_payment_type_display(),
            'date': p.payment_date,
        })

    result = []
    for direction_name in sorted(by_direction.keys()):
        rows = by_direction[direction_name]
        result.append({
            'direction': direction_name,
            'students': rows,
            'total': sum(r['amount'] for r in rows),
        })
    return result


from core.services.teacher_stats import SALARY_PERCENT, get_teacher_report


def teacher_salary_report(year: int, month: int) -> list[dict]:
    """Отчёт по зарплате преподавателей за месяц (посещения × цена, 30%)."""
    start, end = month_bounds(year, month)
    report = []

    for teacher in Teacher.objects.all():
        data = get_teacher_report(teacher, start, end)
        report.append({
            'teacher': teacher.name,
            'visits': data['total_visits'],
            'revenue': data['total_revenue'],
            'salary': data['total_at_percent'],
            'percent': SALARY_PERCENT,
        })

    return report


def monthly_profit_report(year: int, month: int) -> dict:
    """Прибыль/убыток за месяц: доходы − закупки − зарплаты."""
    start, end = month_bounds(year, month)

    income = Payment.objects.filter(
        payment_date__gte=start, payment_date__lte=end,
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    expenses_materials = MaterialPurchase.objects.filter(
        purchase_date__gte=start, purchase_date__lte=end,
    ).aggregate(total=Sum('total_cost'))['total'] or Decimal('0')

    salary_data = teacher_salary_report(year, month)
    expenses_salary = sum(row['salary'] for row in salary_data)

    profit = income - expenses_materials - expenses_salary

    return {
        'year': year,
        'month': month,
        'income': income,
        'expenses_materials': expenses_materials,
        'expenses_salary': expenses_salary,
        'profit': profit,
        'is_profit': profit >= 0,
    }
