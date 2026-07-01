"""
Статистика преподавателя: посещения, начисления, замены и отработки.
"""
from collections import defaultdict
from datetime import date
from decimal import Decimal

from django.utils import timezone

from core.models import (
    AttendanceRecord,
    Direction,
    LessonExceptionType,
    Payment,
    PaymentType,
    ScheduleException,
    SingleLesson,
    SingleLessonType,
    Teacher,
)

SALARY_PERCENT = Decimal('30')


def _parse_dates(date_from: date | None, date_to: date | None) -> tuple[date, date]:
    today = timezone.localdate()
    if not date_from:
        date_from = today.replace(day=1)
    if not date_to:
        date_to = today
    return date_from, date_to


def _teacher_direction_ids(teacher: Teacher) -> set:
    ids = set(teacher.directions.values_list('id', flat=True))
    for slot in teacher.schedule_slots.filter(is_archived=False).values_list('direction_id', flat=True):
        ids.add(slot)
    return ids


def _unit_price(rec: AttendanceRecord) -> Decimal:
    """Абонемент — price_per_lesson, разовое — single_lesson_cost."""
    if rec.single_lesson_id:
        if rec.single_lesson.cost:
            return rec.single_lesson.cost
        return rec.direction.single_lesson_cost
    return rec.direction.price_per_lesson


def _lesson_kind_label(rec: AttendanceRecord) -> str:
    if rec.single_lesson_id:
        if rec.single_lesson.lesson_type == SingleLessonType.MAKEUP:
            return 'Отработка'
        return 'Разовое'
    return 'Абонемент'


def get_teacher_students_by_direction(teacher: Teacher) -> list[dict]:
    direction_ids = _teacher_direction_ids(teacher)
    result = []
    for direction in Direction.objects.filter(id__in=direction_ids).order_by('name'):
        students = list(direction.students.order_by('name'))
        result.append({
            'direction': direction,
            'students': students,
            'students_count': len(students),
        })
    return result


def _teacher_attendance_records(
    teacher: Teacher,
    date_from: date,
    date_to: date,
    direction_ids: list | None = None,
):
    cancelled_pairs = set(
        ScheduleException.objects.filter(
            lesson_date__gte=date_from,
            lesson_date__lte=date_to,
            exception_type=LessonExceptionType.CANCEL,
        ).values_list('lesson_date', 'schedule_slot_id')
    )

    sub_pairs = set(
        ScheduleException.objects.filter(
            lesson_date__gte=date_from,
            lesson_date__lte=date_to,
            exception_type=LessonExceptionType.SUBSTITUTION,
            substitute_teacher=teacher,
        ).values_list('lesson_date', 'schedule_slot_id')
    )

    qs = AttendanceRecord.objects.filter(
        lesson_date__gte=date_from,
        lesson_date__lte=date_to,
    ).select_related(
        'student', 'direction', 'schedule_slot', 'schedule_slot__teacher', 'single_lesson',
    )

    if direction_ids:
        qs = qs.filter(direction_id__in=direction_ids)

    for rec in qs.order_by('-lesson_date', 'student__name'):
        if rec.schedule_slot_id:
            pair = (rec.lesson_date, rec.schedule_slot_id)
            if pair in cancelled_pairs:
                continue
            slot_teacher_id = rec.schedule_slot.teacher_id
            if slot_teacher_id != teacher.id and pair not in sub_pairs:
                continue
        elif rec.single_lesson_id:
            if rec.single_lesson.teacher_id != teacher.id:
                continue
        else:
            continue
        yield rec


def get_teacher_attendance_log(
    teacher: Teacher,
    date_from: date | None = None,
    date_to: date | None = None,
    direction_ids: list | None = None,
) -> list[dict]:
    date_from, date_to = _parse_dates(date_from, date_to)
    rows = []
    for rec in _teacher_attendance_records(teacher, date_from, date_to, direction_ids):
        price = _unit_price(rec)
        rows.append({
            'student_id': rec.student_id,
            'student_name': rec.student.name,
            'date': rec.lesson_date,
            'time': (
                f'{rec.schedule_slot.start_time:%H:%M}–{rec.schedule_slot.end_time:%H:%M}'
                if rec.schedule_slot_id
                else f'{rec.single_lesson.start_time:%H:%M}–{rec.single_lesson.end_time:%H:%M}'
            ),
            'direction_id': rec.direction_id,
            'direction_name': rec.direction.name,
            'present': rec.present,
            'paid': rec.paid,
            'note': rec.note,
            'lesson_type': _lesson_kind_label(rec),
            'unit_price': price,
            'amount': price if rec.present else Decimal('0'),
        })
    return rows


def get_teacher_extras(
    teacher: Teacher,
    date_from: date | None = None,
    date_to: date | None = None,
    direction_ids: list | None = None,
) -> list[dict]:
    date_from, date_to = _parse_dates(date_from, date_to)
    rows = []

    subs = ScheduleException.objects.filter(
        lesson_date__gte=date_from,
        lesson_date__lte=date_to,
        exception_type=LessonExceptionType.SUBSTITUTION,
        substitute_teacher=teacher,
    ).select_related('schedule_slot', 'schedule_slot__direction', 'schedule_slot__teacher')
    if direction_ids:
        subs = subs.filter(schedule_slot__direction_id__in=direction_ids)

    for exc in subs.order_by('-lesson_date'):
        slot = exc.schedule_slot
        orig = slot.teacher.name if slot.teacher else '—'
        rows.append({
            'date': exc.lesson_date,
            'type': 'Замена',
            'type_code': 'substitution',
            'details': (
                f'{slot.start_time:%H:%M}–{slot.end_time:%H:%M} · {slot.direction.name} '
                f'(вместо {orig})'
            ),
            'student_name': None,
            'student_id': None,
            'direction_name': slot.direction.name,
            'direction_id': slot.direction_id,
            'present': None,
            'object_id': exc.id,
        })

    singles = SingleLesson.objects.filter(
        teacher=teacher,
        lesson_date__gte=date_from,
        lesson_date__lte=date_to,
    ).select_related('direction', 'student')
    if direction_ids:
        singles = singles.filter(direction_id__in=direction_ids)

    for sl in singles.order_by('-lesson_date', 'start_time'):
        att = sl.attendance_records.first()
        is_makeup = sl.lesson_type == SingleLessonType.MAKEUP
        rows.append({
            'date': sl.lesson_date,
            'type': 'Отработка' if is_makeup else 'Разовое',
            'type_code': 'makeup' if is_makeup else 'single',
            'details': (
                f'{sl.start_time:%H:%M}–{sl.end_time:%H:%M} · {sl.direction.name}'
                + (f' · {sl.notes}' if sl.notes else '')
            ),
            'student_name': sl.student.name,
            'student_id': sl.student_id,
            'direction_name': sl.direction.name,
            'direction_id': sl.direction_id,
            'present': att.present if att else False,
            'object_id': sl.id,
        })

    rows.sort(key=lambda x: x['date'], reverse=True)
    return rows


def get_teacher_report(
    teacher: Teacher,
    date_from: date | None = None,
    date_to: date | None = None,
    direction_ids: list | None = None,
) -> dict:
    date_from, date_to = _parse_dates(date_from, date_to)

    by_direction: dict = defaultdict(lambda: {
        'direction_name': '',
        'student_visits': 0,
        'revenue': Decimal('0'),
        'students': defaultdict(lambda: {
            'name': '', 'visits': 0, 'paid_visits': 0, 'revenue': Decimal('0'),
        }),
    })
    students_all: dict = defaultdict(lambda: {
        'name': '', 'visits': 0, 'paid_visits': 0, 'total_records': 0, 'revenue': Decimal('0'),
    })

    total_visits = 0
    total_revenue = Decimal('0')

    for rec in _teacher_attendance_records(teacher, date_from, date_to, direction_ids):
        st = students_all[rec.student_id]
        st['name'] = rec.student.name
        st['total_records'] += 1
        if rec.paid:
            st['paid_visits'] += 1

        if not rec.present:
            continue

        price = _unit_price(rec)
        d = rec.direction
        bucket = by_direction[d.id]
        bucket['direction_name'] = d.name
        bucket['student_visits'] += 1
        bucket['revenue'] += price

        dst = bucket['students'][rec.student_id]
        dst['name'] = rec.student.name
        dst['visits'] += 1
        dst['revenue'] += price
        if rec.paid:
            dst['paid_visits'] += 1

        st['visits'] += 1
        st['revenue'] += price
        total_visits += 1
        total_revenue += price

    directions_list = []
    for did, data in sorted(by_direction.items(), key=lambda x: x[1]['direction_name']):
        students_list = [
            {
                'id': sid,
                'name': s['name'],
                'visits': s['visits'],
                'paid_visits': s['paid_visits'],
                'revenue': s['revenue'],
            }
            for sid, s in data['students'].items()
        ]
        directions_list.append({
            'direction_id': did,
            'direction_name': data['direction_name'],
            'student_visits': data['student_visits'],
            'revenue': data['revenue'],
            'students': sorted(students_list, key=lambda x: x['name']),
        })

    students_summary = sorted([
        {
            'id': sid,
            'name': s['name'],
            'visits': s['visits'],
            'paid_visits': s['paid_visits'],
            'total_records': s['total_records'],
            'revenue': s['revenue'],
        }
        for sid, s in students_all.items()
        if s['visits'] > 0 or s['total_records'] > 0
    ], key=lambda x: x['name'])

    total_at_percent = (total_revenue * SALARY_PERCENT / Decimal('100')).quantize(Decimal('0.01'))

    teacher_direction_ids = _teacher_direction_ids(teacher)
    transfers = Payment.objects.filter(
        payment_type__in=[PaymentType.TRANSFER_DEBIT, PaymentType.TRANSFER_CREDIT],
        payment_date__gte=date_from,
        payment_date__lte=date_to,
        direction_id__in=teacher_direction_ids,
    ).select_related('student', 'direction')
    if direction_ids:
        transfers = transfers.filter(direction_id__in=direction_ids)

    transfer_rows = [
        {
            'date': p.payment_date,
            'student': p.student.name,
            'student_id': p.student_id,
            'direction': p.direction.name,
            'direction_id': p.direction_id,
            'amount': p.amount,
            'type': p.get_payment_type_display(),
            'notes': p.notes,
        }
        for p in transfers.order_by('-payment_date')
    ]

    return {
        'directions': directions_list,
        'students_summary': students_summary,
        'total_visits': total_visits,
        'total_revenue': total_revenue,
        'total_at_percent': total_at_percent,
        'salary_percent': SALARY_PERCENT,
        'transfers': transfer_rows,
        'date_from': date_from,
        'date_to': date_to,
        'selected_direction_ids': direction_ids or [],
    }
