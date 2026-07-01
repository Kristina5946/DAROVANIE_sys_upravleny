"""
Сводные данные для страницы «Отчёты».
"""
from decimal import Decimal

from core.services.finance import monthly_profit_report, monthly_payments_by_direction, teacher_salary_report
from core.services.payments_report import get_filtered_payments, get_payments_charts, get_payments_summary
from core.services.schedule import month_bounds

MONTHS_RU = (
    'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
    'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь',
)
MONTHS_SHORT = ('Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек')


def _fmt_money(value) -> str:
    return f'{float(value):,.0f}'.replace(',', ' ')


def _bars(items: list[dict], value_key: str = 'value', limit: int = 12) -> list[dict]:
    sorted_items = sorted(items, key=lambda x: x[value_key], reverse=True)[:limit]
    max_val = max((x[value_key] for x in sorted_items), default=1) or 1
    total = sum(x[value_key] for x in sorted_items) or 1
    result = []
    for item in sorted_items:
        val = item[value_key]
        result.append({
            **item,
            'value_fmt': _fmt_money(val),
            'percent': round(val / total * 100, 1) if total else 0,
            'width': round(val / max_val * 100, 1) if max_val else 0,
        })
    return result


def _shift_month(year: int, month: int, offset: int) -> tuple[int, int]:
    m = month + offset
    y = year
    while m <= 0:
        m += 12
        y -= 1
    while m > 12:
        m -= 12
        y += 1
    return y, m


def get_monthly_trend(end_year: int, end_month: int, months: int = 6) -> list[dict]:
    points = []
    for offset in range(-(months - 1), 1):
        y, m = _shift_month(end_year, end_month, offset)
        profit = monthly_profit_report(y, m)
        points.append({
            'year': y,
            'month': m,
            'label': MONTHS_SHORT[m - 1],
            'label_full': f'{MONTHS_SHORT[m - 1]} {y}',
            'income': float(profit['income']),
            'profit': float(profit['profit']),
            'expenses': float(profit['expenses_materials'] + profit['expenses_salary']),
        })
    max_income = max((p['income'] for p in points), default=1) or 1
    for p in points:
        p['income_width'] = round(p['income'] / max_income * 100, 1)
        p['profit_width'] = round(abs(p['profit']) / max_income * 100, 1)
    return points


def get_reports_dashboard(year: int, month: int) -> dict:
    start, end = month_bounds(year, month)
    profit = monthly_profit_report(year, month)
    salary_rows = teacher_salary_report(year, month)
    payments_qs = get_filtered_payments(date_from=start, date_to=end)
    payments_summary = get_payments_summary(payments_qs)
    payment_charts = get_payments_charts(payments_qs)
    by_direction = monthly_payments_by_direction(year, month)

    salary_chart = _bars([
        {
            'label': row['teacher'],
            'value': float(row['salary']),
            'visits': row['visits'],
            'revenue': float(row['revenue']),
        }
        for row in salary_rows if row['salary'] > 0
    ])

    expense_chart = _bars([
        {'label': 'Доходы (оплаты)', 'value': float(profit['income']), 'kind': 'income'},
        {'label': 'Закупки материалов', 'value': float(profit['expenses_materials']), 'kind': 'expense'},
        {'label': 'Зарплаты (30%)', 'value': float(profit['expenses_salary']), 'kind': 'expense'},
    ])

    salary_total = sum(row['salary'] for row in salary_rows)
    visits_total = sum(row['visits'] for row in salary_rows)
    max_salary = max((float(r['salary']) for r in salary_rows), default=1) or 1
    salary_rows_sorted = sorted(salary_rows, key=lambda r: r['salary'], reverse=True)
    for row in salary_rows_sorted:
        row['salary_width'] = round(float(row['salary']) / max_salary * 100, 1)

    return {
        'year': year,
        'month': month,
        'month_label': MONTHS_RU[month - 1],
        'period_from': start,
        'period_to': end,
        'profit': profit,
        'payments_summary': payments_summary,
        'payment_charts': payment_charts,
        'by_direction': by_direction,
        'salary_rows': salary_rows_sorted,
        'salary_chart': salary_chart,
        'expense_chart': expense_chart,
        'trend': get_monthly_trend(year, month, 6),
        'totals': {
            'salary': salary_total,
            'visits': visits_total,
            'payments_count': payments_summary['count'],
        },
    }
