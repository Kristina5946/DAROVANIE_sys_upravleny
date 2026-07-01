"""
Операции с занятиями на дату: расписание, посещения, разовые, замены.
"""
from dataclasses import dataclass, field
from datetime import date, datetime, time
from decimal import Decimal

from django.db import transaction

from core.models import (
    AttendanceRecord,
    Direction,
    LessonExceptionType,
    LessonType,
    Payment,
    PaymentType,
    ScheduleException,
    ScheduleSlot,
    SingleLesson,
    SingleLessonType,
    Student,
    Teacher,
    WeekDay,
)
from core.services.schedule_day import students_for_slot


@dataclass
class LessonOccurrence:
    """Занятие в конкретный день (регулярное или разовое)."""
    key: str
    lesson_type: str  # regular, single, makeup
    direction: Direction
    teacher: Teacher | None
    start_time: time
    end_time: time
    schedule_slot: ScheduleSlot | None = None
    single_lesson: SingleLesson | None = None
    substitute_teacher: Teacher | None = None
    is_cancelled: bool = False
    students: list[Student] = field(default_factory=list)

    @property
    def display_teacher(self):
        if self.substitute_teacher:
            return self.substitute_teacher
        return self.teacher

    @property
    def title(self):
        suffix = ''
        if self.lesson_type == 'makeup':
            suffix = ' · Отработка'
        elif self.lesson_type == 'single':
            suffix = ' · Разовое'
        if self.is_cancelled:
            suffix += ' · Отмена'
        t = self.display_teacher.name if self.display_teacher else '—'
        return f'{self.direction.name}{suffix} ({self.start_time:%H:%M}–{self.end_time:%H:%M}, {t})'


def _weekday_for_date(d: date) -> int:
    return d.weekday()


def get_teacher_for_slot(slot: ScheduleSlot, lesson_date: date) -> tuple[Teacher | None, Teacher | None, bool]:
    """Возвращает (основной/фактический учитель, заменяющий, отменено)."""
    exc = ScheduleException.objects.filter(
        schedule_slot=slot, lesson_date=lesson_date,
    ).select_related('substitute_teacher').first()
    if exc:
        if exc.exception_type == LessonExceptionType.CANCEL:
            return slot.teacher, None, True
        if exc.exception_type == LessonExceptionType.SUBSTITUTION:
            return exc.substitute_teacher or slot.teacher, exc.substitute_teacher, False
    return slot.teacher, None, False


def get_regular_lessons_on_date(lesson_date: date) -> list[LessonOccurrence]:
    wd = _weekday_for_date(lesson_date)
    slots = (
        ScheduleSlot.objects.filter(day_of_week=wd, is_archived=False)
        .select_related('direction', 'teacher', 'classroom', 'student', 'student__parent')
        .order_by('sort_order', 'start_time')
    )
    result = []
    for slot in slots:
        teacher, sub, cancelled = get_teacher_for_slot(slot, lesson_date)
        students = students_for_slot(slot)
        result.append(LessonOccurrence(
            key=f'slot-{slot.pk}',
            lesson_type='regular',
            direction=slot.direction,
            teacher=teacher,
            start_time=slot.start_time,
            end_time=slot.end_time,
            schedule_slot=slot,
            substitute_teacher=sub,
            is_cancelled=cancelled,
            students=students,
        ))
    return result


def get_single_lessons_on_date(lesson_date: date) -> list[LessonOccurrence]:
    singles = (
        SingleLesson.objects.filter(lesson_date=lesson_date)
        .select_related('student', 'direction', 'teacher', 'classroom')
    )
    result = []
    for sl in singles:
        result.append(LessonOccurrence(
            key=f'single-{sl.pk}',
            lesson_type='makeup' if sl.lesson_type == SingleLessonType.MAKEUP else 'single',
            direction=sl.direction,
            teacher=sl.teacher,
            start_time=sl.start_time,
            end_time=sl.end_time,
            single_lesson=sl,
            students=[sl.student],
        ))
    return result


def get_all_lessons_on_date(lesson_date: date) -> list[LessonOccurrence]:
    lessons = get_regular_lessons_on_date(lesson_date) + get_single_lessons_on_date(lesson_date)
    return sorted(lessons, key=lambda x: x.start_time)


def get_week_schedule() -> dict[int, list[ScheduleSlot]]:
    """Слоты по дням недели 0–6."""
    slots = (
        ScheduleSlot.objects.filter(is_archived=False)
        .select_related('direction', 'teacher', 'classroom')
        .order_by('sort_order', 'start_time')
    )
    week = {i: [] for i in range(7)}
    for s in slots:
        week[s.day_of_week].append(s)
    return week


def _student_paid_for_lesson(student: Student, direction: Direction, lesson_date: date, lesson_type: str) -> bool:
    payments = Payment.objects.filter(student=student, direction=direction)
    for p in payments:
        if p.payment_type == PaymentType.SUBSCRIPTION:
            if p.payment_date.year == lesson_date.year and p.payment_date.month == lesson_date.month:
                return True
        elif p.payment_type in (PaymentType.SINGLE, PaymentType.TRIAL):
            if p.payment_date == lesson_date:
                return True
        elif p.payment_type == PaymentType.TRANSFER_CREDIT:
            if p.payment_date <= lesson_date:
                return True
    return False


def get_or_create_attendance(lesson: LessonOccurrence, lesson_date: date, student: Student) -> AttendanceRecord:
    if lesson.schedule_slot:
        record, created = AttendanceRecord.objects.get_or_create(
            student=student,
            lesson_date=lesson_date,
            schedule_slot=lesson.schedule_slot,
            defaults={
                'direction': lesson.direction,
                'present': False,
                'paid': _student_paid_for_lesson(student, lesson.direction, lesson_date, lesson.lesson_type),
                'note': '',
            },
        )
    else:
        record, created = AttendanceRecord.objects.get_or_create(
            student=student,
            single_lesson=lesson.single_lesson,
            defaults={
                'lesson_date': lesson_date,
                'direction': lesson.direction,
                'present': False,
                'paid': _student_paid_for_lesson(student, lesson.direction, lesson_date, lesson.lesson_type),
                'note': lesson.single_lesson.notes if lesson.single_lesson else '',
            },
        )
    return record


def build_lesson_attendance(lesson: LessonOccurrence, lesson_date: date) -> list[dict]:
    rows = []
    for student in lesson.students:
        rec = get_or_create_attendance(lesson, lesson_date, student)
        rows.append({
            'student': student,
            'record': rec,
            'record_id': str(rec.pk),
        })
    return rows


@transaction.atomic
def save_lesson_attendance(lesson_key: str, lesson_date: date, post_data) -> None:
    """Сохранение посещений из POST (att_present_<id>, att_paid_<id>, att_note_<id>)."""
    for key in post_data:
        if not key.startswith('att_present_'):
            continue
        rec_id = key.replace('att_present_', '')
        try:
            record = AttendanceRecord.objects.get(pk=rec_id)
            record.present = f'att_present_{rec_id}' in post_data
            record.paid = f'att_paid_{rec_id}' in post_data
            record.note = post_data.get(f'att_note_{rec_id}', record.note)
            record.save()
        except AttendanceRecord.DoesNotExist:
            continue


@transaction.atomic
def create_single_lesson_with_payment(
    student: Student,
    direction: Direction,
    teacher: Teacher,
    lesson_date: date,
    start_time: time,
    end_time: time,
    lesson_type: str,
    *,
    create_payment: bool = True,
    notes: str = '',
    created_by=None,
) -> SingleLesson:
    amount = direction.single_lesson_cost
    sl = SingleLesson.objects.create(
        student=student,
        direction=direction,
        teacher=teacher,
        lesson_date=lesson_date,
        start_time=start_time,
        end_time=end_time,
        lesson_type=lesson_type,
        cost=amount,
        notes=notes,
        created_by=created_by,
    )
    AttendanceRecord.objects.create(
        student=student,
        lesson_date=lesson_date,
        single_lesson=sl,
        direction=direction,
        present=False,
        paid=create_payment,
        note=notes or ('Отработка' if lesson_type == SingleLessonType.MAKEUP else 'Разовое'),
    )
    if create_payment:
        ptype = PaymentType.TRIAL if lesson_type == SingleLessonType.MAKEUP else PaymentType.SINGLE
        Payment.objects.create(
            student=student,
            direction=direction,
            payment_date=lesson_date,
            amount=amount,
            payment_type=ptype,
            notes=notes or sl.get_lesson_type_display(),
            created_by=created_by,
        )
    if lesson_type != SingleLessonType.MAKEUP and direction not in student.directions.all():
        student.directions.add(direction)
    return sl


def duplicate_schedule_slot(slot: ScheduleSlot) -> ScheduleSlot:
    max_order = (
        ScheduleSlot.objects.filter(day_of_week=slot.day_of_week)
        .order_by('-sort_order').values_list('sort_order', flat=True).first() or 0
    )
    return ScheduleSlot.objects.create(
        direction=slot.direction,
        subdirection=slot.subdirection,
        day_of_week=slot.day_of_week,
        start_time=slot.start_time,
        end_time=slot.end_time,
        teacher=slot.teacher,
        classroom=slot.classroom,
        sort_order=max_order + 1,
    )
