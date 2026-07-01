from datetime import date, datetime, timedelta
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from accounts.permissions import user_can_view_finance
from core.forms import SearchForm
from core.models import Direction, Payment, Student, Subscription
from core.services.schedule_day import get_lessons_for_date
from core.services.subscriptions import get_subscription_status


MONTHS_RU = ('Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек')


def _monthly_income_chart(months: int = 12) -> list[dict]:
    """Доход по месяцам для графика на главной."""
    today = date.today()
    start = today.replace(day=1) - timedelta(days=months * 31)

    qs = (
        Payment.objects.filter(payment_date__gte=start, amount__gt=0)
        .annotate(month=TruncMonth('payment_date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )
    by_month = {}
    for row in qs:
        m = row['month']
        if not m:
            continue
        if isinstance(m, datetime):
            m = m.date()
        by_month[m] = row['total']

    points = []
    for i in range(months - 1, -1, -1):
        m = today.replace(day=1)
        year, month = m.year, m.month - i
        while month <= 0:
            month += 12
            year -= 1
        key = date(year, month, 1)
        total = by_month.get(key, Decimal('0'))
        points.append({
            'label': MONTHS_RU[key.month - 1],
            'label_full': key.strftime('%m.%Y'),
            'value': float(total),
        })
    return points


def _monthly_income_bars(months: int = 6) -> tuple[list[dict], float]:
    """Столбчатый график доходов для главной."""
    points = _monthly_income_chart(months)
    max_val = max((p['value'] for p in points), default=1) or 1
    bars = []
    for p in points:
        bars.append({
            **p,
            'height_pct': round(p['value'] / max_val * 100, 1) if max_val else 0,
            'value_fmt': f"{p['value']:,.0f}".replace(',', ' '),
        })
    return bars, max_val


@login_required
def home(request):
    today = timezone.localdate()
    month_start = today.replace(day=1)
    is_admin = user_can_view_finance(request.user)

    lessons_today = get_lessons_for_date(today)
    lessons_today_active = [l for l in lessons_today if not l.is_cancelled]

    monthly_income = (
        Payment.objects.filter(payment_date__gte=month_start, amount__gt=0)
        .aggregate(total=Sum('amount'))['total'] or Decimal('0')
    )

    new_students = Student.objects.filter(registration_date__gte=month_start).count()

    stats = {
        'active_subscriptions': Subscription.objects.filter(status='active').count(),
        'new_students': new_students,
        'monthly_income': monthly_income,
        'students': Student.objects.count(),
        'directions': Direction.objects.count(),
    }

    recent_payments = (
        Payment.objects.select_related('student', 'direction')
        .order_by('-payment_date', '-created_at')[:6]
    )

    expiring_subscriptions = (
        Subscription.objects.filter(
            status='active',
            end_date__gte=today,
            end_date__lte=today + timedelta(days=14),
        )
        .select_related('student', 'direction')
        .order_by('end_date')[:6]
    )

    income_bars = []
    income_chart_max = 0
    if is_admin:
        income_bars, income_chart_max = _monthly_income_bars(6)

    schedule_today_url = f"{reverse('core:schedule')}?view=today&date={today.isoformat()}"
    payments_url = (
        f"{reverse('core:payments_report')}?date_from={month_start.isoformat()}&date_to={today.isoformat()}"
    )

    quick_actions = [
        {
            'title': 'Отметить посещение',
            'desc': f'Сегодня {len(lessons_today_active)} занятий',
            'url': schedule_today_url,
            'icon': '✓',
            'accent': 'green',
        },
        {
            'title': 'Добавить ученика',
            'desc': 'Новая карточка + направления',
            'url': reverse('core:student_create'),
            'icon': '👦',
            'accent': 'violet',
        },
        {
            'title': 'Абонементы',
            'desc': 'Продление и остаток занятий',
            'url': reverse('core:subscriptions'),
            'icon': '🎫',
            'accent': 'indigo',
        },
        {
            'title': 'Расписание',
            'desc': 'Неделя, слоты, разовые',
            'url': f"{reverse('core:schedule')}?view=week&edit=1",
            'icon': '📅',
            'accent': 'purple',
        },
        {
            'title': 'Добавить преподавателя',
            'desc': 'Карточка и направления',
            'url': reverse('core:teacher_create'),
            'icon': '👩‍🏫',
            'accent': 'violet',
        },
        {
            'title': 'Направления',
            'desc': 'Цены и описание',
            'url': reverse('core:direction_list'),
            'icon': '🎨',
            'accent': 'indigo',
        },
    ]

    if is_admin:
        quick_actions.insert(1, {
            'title': 'Внести оплату',
            'desc': 'Таблица оплат → «+ Добавить»',
            'url': payments_url,
            'icon': '💳',
            'accent': 'gold',
        })
        quick_actions.append({
            'title': 'Отчёты',
            'desc': 'Доходы, зарплаты, сводка',
            'url': f"{reverse('core:reports_dashboard')}?year={today.year}&month={today.month}",
            'icon': '📊',
            'accent': 'gold',
        })

    nav_shortcuts = [
        {'label': 'Ученики', 'url': reverse('core:student_list')},
        {'label': 'Преподаватели', 'url': reverse('core:teacher_list')},
        {'label': 'Расписание', 'url': reverse('core:schedule')},
        {'label': 'Абонементы', 'url': reverse('core:subscriptions')},
    ]
    if is_admin:
        nav_shortcuts.extend([
            {'label': 'Оплаты', 'url': reverse('core:payments_report')},
            {'label': 'Отчёты', 'url': reverse('core:reports_dashboard')},
        ])

    return render(request, 'pages/home.html', {
        'stats': stats,
        'recent_payments': recent_payments,
        'expiring_subscriptions': expiring_subscriptions,
        'income_bars': income_bars,
        'income_chart_max': income_chart_max,
        'search_form': SearchForm(),
        'today': today,
        'lessons_today_count': len(lessons_today_active),
        'quick_actions': quick_actions,
        'nav_shortcuts': nav_shortcuts,
        'page_title': 'Главная',
    })


@login_required
def subscriptions_grid(request):
    """Сетка абонементов с карточками и полосами прогресса."""
    from django.db.models import Q

    today = date.today()
    form = SearchForm(request.GET or None)
    direction_id = request.GET.get('direction')
    q = request.GET.get('q', '').strip()

    students = Student.objects.prefetch_related('directions').order_by('name')
    if form.is_valid() and form.cleaned_data.get('direction'):
        students = students.filter(directions=form.cleaned_data['direction'])
    elif direction_id:
        students = students.filter(directions__id=direction_id)
    if q:
        students = students.filter(
            Q(name__icontains=q) | Q(parent__name__icontains=q) | Q(parent__phone__icontains=q),
        )

    cards = []
    for student in students:
        for direction in student.directions.all():
            subs = student.subscriptions.filter(
                direction=direction,
                start_date__year=today.year,
                start_date__month=today.month,
                status='active',
            )
            for sub in subs:
                cards.append(get_subscription_status(sub))
            if not subs.exists():
                cards.append({
                    'subscription': None,
                    'student': student,
                    'direction': direction,
                    'used': 0,
                    'total': 0,
                    'remaining': 0,
                    'percent': 0,
                    'color': 'muted',
                    'amount_paid': 0,
                    'amount_used': 0,
                    'balance': 0,
                })

    return render(request, 'pages/subscriptions.html', {
        'cards': cards,
        'search_form': form,
        'selected_direction': direction_id,
        'page_title': 'Абонементы',
        'total_count': len(cards),
    })
