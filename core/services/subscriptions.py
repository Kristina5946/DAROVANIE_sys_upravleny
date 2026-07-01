"""
Создание и расчёт абонементов.
Исправляет проблему Streamlit-версии: при покупке фиксируется total_lessons
и создаются записи посещений с paid=True.
"""
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP

from django.db import transaction

from core.models import (
    AttendanceRecord,
    Direction,
    Payment,
    PaymentType,
    Student,
    Subscription,
    SubscriptionStatus,
)
from core.services.schedule import count_lessons_in_month, get_month_lesson_dates, get_slots_for_date, month_bounds


def estimate_amount_for_lessons(
    direction: Direction,
    lessons_count: int,
    payment_date: date | None = None,
) -> Decimal:
    """Сумма = цена за занятие (абонемент) × количество."""
    if lessons_count <= 0:
        return Decimal('0')
    if direction.price_per_lesson and direction.price_per_lesson > 0:
        return (direction.price_per_lesson * lessons_count).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    payment_date = payment_date or date.today()
    lessons_in_month = count_lessons_in_month(direction.id, payment_date.year, payment_date.month)
    if lessons_in_month <= 0:
        lessons_in_month = 8
    cost_per = direction.subscription_cost / Decimal(lessons_in_month)
    return (cost_per * lessons_count).quantize(Decimal('1'), rounding=ROUND_HALF_UP)


def get_active_subscription(student: Student, direction: Direction) -> Subscription | None:
    today = date.today()
    return (
        student.subscriptions.filter(
            direction=direction,
            status=SubscriptionStatus.ACTIVE,
            start_date__lte=today,
            end_date__gte=today,
        )
        .order_by('-start_date')
        .first()
    )


def get_direction_card(student: Student, direction: Direction) -> dict:
    """Карточка направления на странице ученика."""
    sub = get_active_subscription(student, direction)
    if sub:
        card = get_subscription_status(sub)
        card['direction'] = direction
        card['has_subscription'] = True
        return card
    return {
        'subscription': None,
        'student': student,
        'direction': direction,
        'has_subscription': False,
        'used': 0,
        'total': 0,
        'remaining': 0,
        'percent': 0,
        'color': 'muted',
        'amount_paid': Decimal('0'),
        'amount_used': Decimal('0'),
        'balance': Decimal('0'),
        'suggested_lessons': count_lessons_in_month(
            direction.id, date.today().year, date.today().month,
        ) or 8,
        'suggested_amount': estimate_amount_for_lessons(
            direction,
            count_lessons_in_month(direction.id, date.today().year, date.today().month) or 8,
        ),
    }


def get_direction_student_cards(direction: Direction) -> list[dict]:
    """Карточки учеников направления для страницы детализации."""
    from core.models import Payment

    students = direction.students.select_related('parent').order_by('name')
    cards = []
    for student in students:
        card = get_direction_card(student, direction)
        last_payment = (
            Payment.objects.filter(student=student, direction=direction)
            .order_by('-payment_date')
            .first()
        )
        card['student'] = student
        card['last_payment'] = last_payment
        cards.append(card)
    return cards


@transaction.atomic
def create_subscription_with_payment(
    student: Student,
    direction: Direction,
    payment_date: date,
    amount: Decimal,
    *,
    carried_lessons: int = 0,
    notes: str = '',
    created_by=None,
) -> tuple[Payment, Subscription]:
    """
    Покупка абонемента:
    1. Создаёт оплату
    2. Создаёт абонемент с total_lessons по расписанию
    3. Создаёт записи посещений на все даты месяца (paid=True)
    """
    year, month = payment_date.year, payment_date.month
    start_date, end_date = month_bounds(year, month)
    total_lessons = count_lessons_in_month(direction.id, year, month)

    payment = Payment.objects.create(
        student=student,
        direction=direction,
        payment_date=payment_date,
        amount=amount,
        payment_type=PaymentType.SUBSCRIPTION,
        notes=notes or 'Абонемент',
        created_by=created_by,
    )

    subscription = Subscription.objects.create(
        student=student,
        direction=direction,
        payment=payment,
        start_date=start_date,
        end_date=end_date,
        total_lessons=total_lessons,
        carried_lessons=carried_lessons,
        amount=amount,
        status=SubscriptionStatus.ACTIVE,
        notes=notes,
    )

    _create_attendance_for_subscription(subscription)
    return payment, subscription


@transaction.atomic
def create_custom_subscription(
    student: Student,
    direction: Direction,
    payment_date: date,
    amount: Decimal,
    total_lessons: int,
    *,
    carried_lessons: int = 0,
    notes: str = '',
    created_by=None,
) -> tuple[Payment, Subscription]:
    """Пополнение абонемента с явным количеством занятий."""
    start_date, default_end = month_bounds(payment_date.year, payment_date.month)

    payment = Payment.objects.create(
        student=student,
        direction=direction,
        payment_date=payment_date,
        amount=amount,
        payment_type=PaymentType.SUBSCRIPTION,
        notes=notes or 'Абонемент',
        created_by=created_by,
    )

    subscription = Subscription.objects.create(
        student=student,
        direction=direction,
        payment=payment,
        start_date=start_date,
        end_date=default_end,
        total_lessons=total_lessons,
        carried_lessons=carried_lessons,
        amount=amount,
        status=SubscriptionStatus.ACTIVE,
        notes=notes,
    )

    last_date = _create_attendance_for_custom_subscription(subscription, total_lessons + carried_lessons)
    if last_date and last_date > subscription.end_date:
        subscription.end_date = last_date
        subscription.save(update_fields=['end_date', 'updated_at'])

    return payment, subscription


def _create_attendance_for_custom_subscription(
    subscription: Subscription,
    slots_needed: int,
) -> date | None:
    """Создаёт записи посещений на N ближайших занятий по расписанию."""
    created = 0
    last_date = None
    start = subscription.start_date

    for month_offset in range(0, 6):
        y = start.year + (start.month + month_offset - 1) // 12
        m = (start.month + month_offset - 1) % 12 + 1
        for lesson_date in sorted(get_month_lesson_dates(subscription.direction_id, y, m)):
            if lesson_date < start:
                continue
            for slot in get_slots_for_date(subscription.direction_id, lesson_date, subscription.student_id):
                if created >= slots_needed:
                    return last_date
                _, was_created = AttendanceRecord.objects.get_or_create(
                    student=subscription.student,
                    lesson_date=lesson_date,
                    schedule_slot=slot,
                    defaults={
                        'direction': subscription.direction,
                        'subscription': subscription,
                        'present': False,
                        'paid': True,
                        'note': 'Абонемент',
                    },
                )
                if was_created:
                    created += 1
                    last_date = lesson_date
    return last_date


def _create_attendance_for_subscription(subscription: Subscription) -> int:
    """Создаёт записи посещений на все плановые даты абонемента."""
    created = 0
    year = subscription.start_date.year
    month = subscription.start_date.month
    lesson_dates = get_month_lesson_dates(subscription.direction_id, year, month)

    for lesson_date in lesson_dates:
        if lesson_date < subscription.start_date or lesson_date > subscription.end_date:
            continue
        slots = get_slots_for_date(subscription.direction_id, lesson_date, subscription.student_id)
        for slot in slots:
            _, was_created = AttendanceRecord.objects.get_or_create(
                student=subscription.student,
                lesson_date=lesson_date,
                schedule_slot=slot,
                defaults={
                    'direction': subscription.direction,
                    'subscription': subscription,
                    'present': False,
                    'paid': True,
                    'note': 'Абонемент',
                },
            )
            if was_created:
                created += 1
    return created


def get_subscription_status(subscription: Subscription) -> dict:
    """Данные для карточки абонемента с полосой прогресса."""
    used = subscription.lessons_used()
    total = subscription.lessons_available
    remaining = subscription.lessons_remaining()
    percent = subscription.usage_percent()

    if percent >= 100:
        color = 'danger'
    elif percent >= 75:
        color = 'warning'
    else:
        color = 'success'

    cost_per_lesson = (
        subscription.amount / total if total > 0 else Decimal('0')
    )
    used_amount = cost_per_lesson * used
    balance = subscription.amount - used_amount

    return {
        'subscription': subscription,
        'used': used,
        'total': total,
        'remaining': remaining,
        'percent': percent,
        'color': color,
        'amount_paid': subscription.amount,
        'amount_used': used_amount,
        'balance': balance,
    }


def get_student_subscriptions_for_month(student: Student, year: int, month: int):
    """Активные абонементы ученика в указанном месяце."""
    start, end = month_bounds(year, month)
    return Subscription.objects.filter(
        student=student,
        start_date__lte=end,
        end_date__gte=start,
        status=SubscriptionStatus.ACTIVE,
    ).select_related('direction')


def mark_attendance_present(record: AttendanceRecord, present: bool, note: str = '') -> None:
    record.present = present
    if note:
        record.note = note
    record.save(update_fields=['present', 'note', 'updated_at'])
