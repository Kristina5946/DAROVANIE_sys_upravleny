"""
Расчёт дат занятий по расписанию.
Перенесено из app.py: get_month_lessons, calculate_lessons_in_month.
"""
import calendar
from datetime import date, datetime, time

from django.db.models import Q

from core.models import Direction, ScheduleSlot, WeekDay, LessonType


DAY_MAP_RU = {choice.value: choice.label for choice in WeekDay}


def _effective_q(lesson_date: date) -> Q:
    """Фильтр слотов, действующих на lesson_date. null = бессрочно."""
    return (
        (Q(effective_from__isnull=True) | Q(effective_from__lte=lesson_date))
        & (Q(effective_to__isnull=True) | Q(effective_to__gte=lesson_date))
    )


def active_slots_qs(lesson_date: date | None = None):
    qs = ScheduleSlot.objects.filter(is_archived=False)
    if lesson_date:
        qs = qs.filter(_effective_q(lesson_date))
    return qs


def get_direction_weekdays(direction_id, lesson_date: date | None = None) -> set[int]:
    """Дни недели (0=Пн), когда идёт направление (с учётом версионирования)."""
    qs = ScheduleSlot.objects.filter(direction_id=direction_id, is_archived=False)
    if lesson_date:
        qs = qs.filter(_effective_q(lesson_date))
    return set(qs.values_list('day_of_week', flat=True))


def get_month_lesson_dates(direction_id, year: int, month: int) -> list[date]:
    """Все даты занятий направления в указанном месяце по расписанию с учётом effective диапазона."""
    _, num_days = calendar.monthrange(year, month)
    dates = []
    for day in range(1, num_days + 1):
        d = date(year, month, day)
        wd = d.weekday()
        if not ScheduleSlot.objects.filter(
            direction_id=direction_id,
            day_of_week=wd,
            is_archived=False,
        ).filter(_effective_q(d)).exists():
            continue
        dates.append(d)
    return dates


def count_lessons_in_month(direction_id, year: int, month: int) -> int:
    return len(get_month_lesson_dates(direction_id, year, month))


def get_slots_for_date(direction_id, lesson_date: date, student_id=None):
    """Слоты расписания направления на день недели с учётом версионирования."""
    qs = ScheduleSlot.objects.filter(
        direction_id=direction_id,
        day_of_week=lesson_date.weekday(),
        is_archived=False,
    ).filter(_effective_q(lesson_date)).select_related('teacher', 'classroom', 'student', 'direction')
    direction = Direction.objects.filter(pk=direction_id).only('lesson_type').first()
    if direction and direction.lesson_type == LessonType.INDIVIDUAL and student_id:
        qs = qs.filter(student_id=student_id)
    return qs


def month_bounds(year: int, month: int) -> tuple[date, date]:
    _, last_day = calendar.monthrange(year, month)
    return date(year, month, 1), date(year, month, last_day)


def safe_time_parse(time_str: str) -> time:
    for fmt in ('%H:%M', '%H:%M:%S', '%H.%M'):
        try:
            return datetime.strptime(time_str, fmt).time()
        except ValueError:
            continue
    return time.min
