from datetime import date

from django.shortcuts import redirect, render

from core.decorators import admin_required
from core.services.reports_dashboard import MONTHS_RU, get_reports_dashboard


@admin_required
def reports_dashboard(request):
    today = date.today()
    try:
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))
        if not (1 <= month <= 12):
            raise ValueError
    except (TypeError, ValueError):
        year, month = today.year, today.month

    dashboard = get_reports_dashboard(year, month)

    return render(request, 'pages/reports/index.html', {
        'dashboard': dashboard,
        'year': year,
        'month': month,
        'month_labels': list(enumerate(MONTHS_RU, start=1)),
        'year_choices': list(range(today.year - 2, today.year + 1)),
        'page_title': 'Отчёты',
    })


@admin_required
def profit_report(request):
    """Обратная совместимость — перенаправление на сводку."""
    qs = request.GET.urlencode()
    url = '/reports/'
    if qs:
        url += f'?{qs}'
    return redirect(url)


@admin_required
def salary_report(request):
    """Обратная совместимость — перенаправление на сводку."""
    qs = request.GET.urlencode()
    url = '/reports/#salary'
    if qs:
        url = f'/reports/?{qs}#salary'
    return redirect(url)
