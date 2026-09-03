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
from core.services.schedule import (
    count_lessons_in_month,
    get_direction_weekdays,
    get_month_lesson_dates,
    get_slots_for_date,
    month_bounds,
)


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


def _active_subscriptions_qs(student: Student, direction: Direction):
    """Активные абонементы по направлению в порядке списания."""
    return (
        student.subscriptions.filter(
            direction=direction,
            status=SubscriptionStatus.ACTIVE,
        )
        .order_by('start_date', 'created_at')
    )


def get_subscription_for_attendance(
    student: Student,
    direction: Direction,
    lesson_date: date,
) -> Subscription | None:
    """
    Абонемент, с которого списывается посещение.
    Первый активный в очереди с остатком занятий; если все исчерпаны — последний подходящий по дате.
    """
    in_range = [
        sub for sub in _active_subscriptions_qs(student, direction)
        if sub.start_date <= lesson_date <= sub.end_date
    ]
    for sub in in_range:
        if sub.lessons_remaining() > 0:
            return sub
    return in_range[-1] if in_range else None


def get_active_subscription(student: Student, direction: Direction) -> Subscription | None:
    """Текущий абонемент для отображения (тот, с которого сейчас списываются занятия)."""
    today = date.today()
    return get_subscription_for_attendance(student, direction, today)


def get_queued_subscriptions(student: Student, direction: Direction) -> list[Subscription]:
    """Абонементы в очереди — активные, но не текущие для списания."""
    primary = get_active_subscription(student, direction)
    subs = list(_active_subscriptions_qs(student, direction))
    if not primary:
        return subs[1:] if len(subs) > 1 else []
    return [sub for sub in subs if sub.pk != primary.pk]


def resolve_subscription_period(
    payment_date: date,
    from_month_start: bool,
    *,
    from_next_month: bool = False,
) -> tuple[date, date]:
    """Период абонемента: с даты оплаты, с 1-го числа месяца или со следующего месяца."""
    if from_next_month:
        if payment_date.month == 12:
            start = date(payment_date.year + 1, 1, 1)
        else:
            start = date(payment_date.year, payment_date.month + 1, 1)
        _, end = month_bounds(start.year, start.month)
        return start, end
    month_start, month_end = month_bounds(payment_date.year, payment_date.month)
    if from_month_start:
        return month_start, month_end
    return payment_date, month_end


def calculate_subscription_end_date(
    direction_id,
    start_date: date,
    lessons_count: int,
    *,
    student_id=None,
    max_months_ahead: int = 18,
) -> date:
    """
    Дата N-го занятия по расписанию, начиная с start_date.
    Если расписания нет — последний день месяца start_date.
    """
    if lessons_count <= 0:
        _, month_end = month_bounds(start_date.year, start_date.month)
        return month_end

    if not get_direction_weekdays(direction_id):
        _, month_end = month_bounds(start_date.year, start_date.month)
        return month_end

    counted = 0
    last_date = None

    for month_offset in range(max_months_ahead):
        y = start_date.year + (start_date.month + month_offset - 1) // 12
        m = (start_date.month + month_offset - 1) % 12 + 1
        for lesson_date in sorted(get_month_lesson_dates(direction_id, y, m)):
            if lesson_date < start_date:
                continue
            slots = list(get_slots_for_date(direction_id, lesson_date, student_id))
            if not slots:
                continue
            for _slot in slots:
                counted += 1
                last_date = lesson_date
                if counted >= lessons_count:
                    return lesson_date

    if last_date:
        return last_date
    _, month_end = month_bounds(start_date.year, start_date.month)
    return month_end


def _link_existing_attendance_for_subscription(subscription: Subscription) -> int:
    """Привязать регулярные посещения по расписанию, которые должны списываться с этого абонемента."""
    unlinked = AttendanceRecord.objects.filter(
        student=subscription.student,
        direction=subscription.direction,
        lesson_date__gte=subscription.start_date,
        lesson_date__lte=subscription.end_date,
        subscription__isnull=True,
        single_lesson__isnull=True,
        schedule_slot__isnull=False,
    )
    linked = 0
    for record in unlinked:
        consumer = get_subscription_for_attendance(
            subscription.student,
            subscription.direction,
            record.lesson_date,
        )
        if not consumer or consumer.pk != subscription.pk:
            continue
        record.subscription = subscription
        if record.present:
            record.paid = True
        if not record.note:
            record.note = 'Абонемент'
        record.save(update_fields=['subscription', 'paid', 'note', 'updated_at'])
        linked += 1
    return linked


def link_attendance_to_active_subscription(record: AttendanceRecord) -> None:
    """При сохранении посещения — привязать к нужному абонементу или отвязать разовое/отработку."""
    if record.single_lesson_id:
        if record.subscription_id:
            record.subscription = None
            record.save(update_fields=['subscription', 'updated_at'])
        return

    sub = get_subscription_for_attendance(
        record.student,
        record.direction,
        record.lesson_date,
    )
    if not sub:
        if record.subscription_id:
            record.subscription = None
            record.save(update_fields=['subscription', 'updated_at'])
        return

    changed_fields = []
    if record.subscription_id != sub.id:
        record.subscription = sub
        changed_fields.append('subscription')
    if record.present and not record.paid:
        record.paid = True
        changed_fields.append('paid')
    if not record.note:
        record.note = 'Абонемент'
        changed_fields.append('note')
    if changed_fields:
        changed_fields.append('updated_at')
        record.save(update_fields=changed_fields)


def _get_or_link_attendance_record(
    subscription: Subscription,
    lesson_date: date,
    schedule_slot,
) -> tuple[AttendanceRecord, bool]:
    record = AttendanceRecord.objects.filter(
        student=subscription.student,
        lesson_date=lesson_date,
        schedule_slot=schedule_slot,
    ).first()
    if record:
        changed = False
        if record.subscription_id != subscription.id:
            record.subscription = subscription
            changed = True
        if not record.paid:
            record.paid = True
            changed = True
        if not record.note:
            record.note = 'Абонемент'
            changed = True
        if changed:
            record.save(update_fields=['subscription', 'paid', 'note', 'updated_at'])
        return record, False

    record = AttendanceRecord.objects.create(
        student=subscription.student,
        lesson_date=lesson_date,
        schedule_slot=schedule_slot,
        direction=subscription.direction,
        subscription=subscription,
        present=False,
        paid=True,
        note='Абонемент',
    )
    return record, True


def get_direction_card(student: Student, direction: Direction) -> dict:
    """Карточка направления на странице ученика."""
    sub = get_active_subscription(student, direction)
    queued = get_queued_subscriptions(student, direction)
    if sub:
        _link_existing_attendance_for_subscription(sub)
        for queued_sub in queued:
            _link_existing_attendance_for_subscription(queued_sub)
        card = get_subscription_status(sub)
        card['direction'] = direction
        card['has_subscription'] = True
        card['queued_subscriptions'] = [
            {**get_subscription_status(qs), 'subscription': qs, 'is_queued': True}
            for qs in queued
        ]
        return card
    return {
        'subscription': None,
        'student': student,
        'direction': direction,
        'has_subscription': bool(queued),
        'queued_subscriptions': [
            {**get_subscription_status(qs), 'subscription': qs, 'is_queued': True}
            for qs in queued
        ],
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
    from_month_start: bool = True,
    from_next_month: bool = False,
) -> tuple[Payment, Subscription]:
    """
    Покупка абонемента:
    1. Создаёт оплату
    2. Создаёт абонемент с total_lessons по расписанию
    3. Создаёт записи посещений на все даты месяца (paid=True)
    """
    start_date, _default_end = resolve_subscription_period(
        payment_date, from_month_start, from_next_month=from_next_month,
    )
    year, month = start_date.year, start_date.month
    total_lessons = count_lessons_in_month(direction.id, year, month)
    end_date = calculate_subscription_end_date(
        direction.id, start_date, total_lessons + carried_lessons, student_id=student.id,
    )

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
    _link_existing_attendance_for_subscription(subscription)
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
    from_month_start: bool = True,
    from_next_month: bool = False,
    end_date: date | None = None,
) -> tuple[Payment, Subscription]:
    """Пополнение / новый абонемент в очереди с явным количеством занятий."""
    start_date, _default_end = resolve_subscription_period(
        payment_date, from_month_start, from_next_month=from_next_month,
    )
    lessons_total = total_lessons + carried_lessons
    if end_date is None:
        end_date = calculate_subscription_end_date(
            direction.id, start_date, lessons_total, student_id=student.id,
        )

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

    last_date = _create_attendance_for_custom_subscription(subscription, lessons_total)
    _link_existing_attendance_for_subscription(subscription)
    if last_date and last_date > subscription.end_date:
        subscription.end_date = last_date
        subscription.save(update_fields=['end_date', 'updated_at'])

    return payment, subscription


def _create_attendance_for_custom_subscription(
    subscription: Subscription,
    slots_needed: int,
) -> date | None:
    """Создаёт записи посещений на N ближайших занятий по расписанию."""
    _link_existing_attendance_for_subscription(subscription)
    already = subscription.attendance_records.count()
    if already >= slots_needed:
        return subscription.attendance_records.order_by('-lesson_date').values_list('lesson_date', flat=True).first()

    need = slots_needed - already
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
                if created >= need:
                    return last_date
                record, was_created = _get_or_link_attendance_record(subscription, lesson_date, slot)
                if was_created:
                    created += 1
                    last_date = lesson_date
                elif record.lesson_date and (last_date is None or record.lesson_date > last_date):
                    last_date = record.lesson_date
    return last_date


def _create_attendance_for_subscription(subscription: Subscription) -> int:
    """Создаёт записи посещений на все плановые даты абонемента."""
    _link_existing_attendance_for_subscription(subscription)
    created = 0
    year = subscription.start_date.year
    month = subscription.start_date.month
    lesson_dates = get_month_lesson_dates(subscription.direction_id, year, month)

    for lesson_date in lesson_dates:
        if lesson_date < subscription.start_date or lesson_date > subscription.end_date:
            continue
        slots = get_slots_for_date(subscription.direction_id, lesson_date, subscription.student_id)
        for slot in slots:
            _, was_created = _get_or_link_attendance_record(subscription, lesson_date, slot)
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


def sync_subscription_from_payment(payment: Payment) -> None:
    """Обновить сумму абонемента при изменении связанной оплаты."""
    sub = Subscription.objects.filter(payment=payment).first()
    if not sub:
        return
    sub.amount = payment.amount
    sub.save(update_fields=['amount', 'updated_at'])


def _ensure_attendance_slot_count(subscription: Subscription, target_count: int) -> date | None:
    """Добавить записи посещений, если их меньше target_count."""
    current = subscription.attendance_records.count()
    if current >= target_count:
        return None
    need = target_count - current
    created = 0
    last_date = None
    start = subscription.start_date

    for month_offset in range(0, 12):
        y = start.year + (start.month + month_offset - 1) // 12
        m = (start.month + month_offset - 1) % 12 + 1
        for lesson_date in sorted(get_month_lesson_dates(subscription.direction_id, y, m)):
            if lesson_date < start:
                continue
            for slot in get_slots_for_date(subscription.direction_id, lesson_date, subscription.student_id):
                if created >= need:
                    return last_date
                record, was_created = _get_or_link_attendance_record(subscription, lesson_date, slot)
                if was_created:
                    created += 1
                    last_date = lesson_date
    return last_date


def _trim_attendance_slots(subscription: Subscription, target_count: int) -> None:
    """Удалить лишние неиспользованные записи посещений."""
    current = subscription.attendance_records.count()
    if current <= target_count:
        return
    to_remove = current - target_count
    removable = list(
        subscription.attendance_records.filter(present=False).order_by('-lesson_date')[:to_remove]
    )
    if len(removable) < to_remove:
        used = subscription.lessons_used()
        raise ValueError(
            f'Нельзя уменьшить число занятий: уже отмечено {used} посещений. '
            f'Минимум — {used} занятий.'
        )
    for record in removable:
        record.delete()


@transaction.atomic
def update_subscription(
    subscription: Subscription,
    *,
    total_lessons: int,
    carried_lessons: int,
    amount: Decimal,
    start_date: date,
    end_date: date,
    payment_date: date | None = None,
    notes: str = '',
    auto_end_date: bool = False,
) -> Subscription:
    """Редактирование абонемента с синхронизацией оплаты и посещений."""
    lessons_available = total_lessons + carried_lessons
    used = subscription.lessons_used()
    if lessons_available < used:
        raise ValueError(
            f'Уже отмечено {used} посещений — нельзя установить меньше {used} занятий.'
        )

    if auto_end_date:
        end_date = calculate_subscription_end_date(
            subscription.direction_id,
            start_date,
            lessons_available,
            student_id=subscription.student_id,
        )

    subscription.total_lessons = total_lessons
    subscription.carried_lessons = carried_lessons
    subscription.amount = amount
    subscription.start_date = start_date
    subscription.end_date = end_date
    subscription.notes = notes
    subscription.save()

    if subscription.payment_id:
        payment = subscription.payment
        payment.amount = amount
        if payment_date:
            payment.payment_date = payment_date
        if notes:
            payment.notes = notes
        payment.payment_type = PaymentType.SUBSCRIPTION
        payment.save(update_fields=['amount', 'payment_date', 'notes', 'payment_type', 'updated_at'])

    _trim_attendance_slots(subscription, lessons_available)
    last_date = _ensure_attendance_slot_count(subscription, lessons_available)
    _link_existing_attendance_for_subscription(subscription)
    if last_date and last_date > subscription.end_date:
        subscription.end_date = last_date
        subscription.save(update_fields=['end_date', 'updated_at'])

    return subscription
