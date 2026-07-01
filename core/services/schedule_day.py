"""
Занятия на дату, посещения, разовые и отработки.
"""
from dataclasses import dataclass, field
from datetime import date, time
from decimal import Decimal
from typing import Literal
from uuid import UUID

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
)


LessonKind = Literal['regular', 'single', 'makeup']


@dataclass
class DayLesson:
    key: str
    kind: LessonKind
    schedule_slot: ScheduleSlot | None
    single_lesson: SingleLesson | None
    direction: Direction
    teacher: Teacher | None
    substitute_teacher: Teacher | None
    is_cancelled: bool
    start_time: time
    end_time: time
    students: list[Student] = field(default_factory=list)
    exception: ScheduleException | None = None

    @property
    def display_teacher(self) -> Teacher | None:
        if self.substitute_teacher:
            return self.substitute_teacher
        return self.teacher

    @property
    def title(self) -> str:
        suffix = ''
        if self.kind == 'single':
            suffix = ' (разовое)'
        elif self.kind == 'makeup':
            suffix = ' (отработка)'
        name = self.direction.name
        if (
            self.kind == 'regular'
            and self.direction.lesson_type == LessonType.INDIVIDUAL
            and self.students
        ):
            name = f'{name} — {self.students[0].name}'
        elif (
            self.kind == 'regular'
            and self.direction.lesson_type == LessonType.INDIVIDUAL
            and not self.students
        ):
            name = f'{name} (ученик не назначен)'
        return f'{name}{suffix}'


def students_for_slot(slot: ScheduleSlot) -> list[Student]:
    """Группа — все ученики направления; индивидуальное — один назначенный ученик."""
    if slot.direction.lesson_type == LessonType.INDIVIDUAL:
        if slot.student_id:
            return [slot.student]
        return []
    return list(
        slot.direction.students.select_related('parent').order_by('name')
    )


def get_lessons_for_date(lesson_date: date) -> list[DayLesson]:
    """Регулярные слоты на день недели + разовые на дату."""
    weekday = lesson_date.weekday()
    lessons: list[DayLesson] = []

    slots = (
        ScheduleSlot.objects.filter(day_of_week=weekday, is_archived=False)
        .select_related('direction', 'teacher', 'classroom', 'student', 'student__parent')
        .order_by('sort_order', 'start_time')
    )
    exceptions = {
        (e.schedule_slot_id, e.lesson_date): e
        for e in ScheduleException.objects.filter(lesson_date=lesson_date).select_related(
            'substitute_teacher', 'schedule_slot',
        )
    }

    for slot in slots:
        exc = exceptions.get((slot.id, lesson_date))
        is_cancelled = exc is not None and exc.exception_type == LessonExceptionType.CANCEL
        sub_teacher = exc.substitute_teacher if exc and exc.exception_type == LessonExceptionType.SUBSTITUTION else None
        students = students_for_slot(slot)
        lessons.append(DayLesson(
            key=f'regular-{slot.id}',
            kind='regular',
            schedule_slot=slot,
            single_lesson=None,
            direction=slot.direction,
            teacher=slot.teacher,
            substitute_teacher=sub_teacher,
            is_cancelled=is_cancelled,
            start_time=slot.start_time,
            end_time=slot.end_time,
            students=students,
            exception=exc,
        ))

    singles = (
        SingleLesson.objects.filter(lesson_date=lesson_date)
        .select_related('student', 'direction', 'teacher', 'student__parent')
        .order_by('start_time')
    )
    for sl in singles:
        kind: LessonKind = 'makeup' if sl.lesson_type == SingleLessonType.MAKEUP else 'single'
        lessons.append(DayLesson(
            key=f'single-{sl.id}',
            kind=kind,
            schedule_slot=None,
            single_lesson=sl,
            direction=sl.direction,
            teacher=sl.teacher,
            substitute_teacher=None,
            is_cancelled=False,
            start_time=sl.start_time,
            end_time=sl.end_time,
            students=[sl.student],
            exception=None,
        ))

    lessons.sort(key=lambda x: x.start_time)
    return lessons


def get_attendance_for_lesson(lesson: DayLesson, lesson_date: date) -> dict[UUID, AttendanceRecord]:
    """Записи посещений для занятия (создаёт недостающие)."""
    records = {}
    for student in lesson.students:
        if lesson.schedule_slot:
            rec, _ = AttendanceRecord.objects.get_or_create(
                student=student,
                lesson_date=lesson_date,
                schedule_slot=lesson.schedule_slot,
                defaults={
                    'direction': lesson.direction,
                    'present': False,
                    'paid': _default_paid(student, lesson.direction, lesson_date),
                    'note': '',
                },
            )
        else:
            rec, _ = AttendanceRecord.objects.get_or_create(
                student=student,
                single_lesson=lesson.single_lesson,
                defaults={
                    'lesson_date': lesson_date,
                    'direction': lesson.direction,
                    'present': False,
                    'paid': lesson.kind == 'makeup',
                    'note': lesson.single_lesson.notes or '',
                },
            )
        records[student.id] = rec
    return records


def _default_paid(student: Student, direction: Direction, lesson_date: date) -> bool:
    return Payment.objects.filter(
        student=student,
        direction=direction,
        payment_type=PaymentType.SUBSCRIPTION,
        payment_date__year=lesson_date.year,
        payment_date__month=lesson_date.month,
    ).exists()


@transaction.atomic
def save_lesson_attendance(
    lesson: DayLesson,
    lesson_date: date,
    student_data: list[dict],
) -> None:
    """student_data: [{student_id, present, paid, note}]"""
    records = get_attendance_for_lesson(lesson, lesson_date)
    for row in student_data:
        sid_raw = row['student_id']
        sid = sid_raw if isinstance(sid_raw, UUID) else UUID(str(sid_raw))
        if sid not in records:
            continue
        rec = records[sid]
        rec.present = row.get('present', False)
        rec.paid = row.get('paid', False)
        rec.note = row.get('note', '')[:500]
        rec.save(update_fields=['present', 'paid', 'note', 'updated_at'])


@transaction.atomic
def add_single_or_makeup(
    *,
    student: Student,
    direction: Direction,
    teacher: Teacher,
    lesson_date: date,
    start_time,
    end_time,
    lesson_type: str,
    create_payment: bool,
    payment_amount: Decimal | None,
    notes: str,
    created_by,
) -> SingleLesson:
    sl = SingleLesson.objects.create(
        student=student,
        direction=direction,
        teacher=teacher,
        lesson_date=lesson_date,
        start_time=start_time,
        end_time=end_time,
        lesson_type=lesson_type,
        cost=payment_amount,
        notes=notes,
        created_by=created_by,
    )
    AttendanceRecord.objects.create(
        student=student,
        lesson_date=lesson_date,
        single_lesson=sl,
        direction=direction,
        present=False,
        paid=lesson_type == SingleLessonType.MAKEUP or create_payment,
        note=notes,
    )
    if create_payment and payment_amount and payment_amount > 0:
        ptype = PaymentType.SINGLE if lesson_type == SingleLessonType.SINGLE else PaymentType.OTHER
        Payment.objects.create(
            student=student,
            direction=direction,
            payment_date=lesson_date,
            amount=payment_amount,
            payment_type=ptype,
            notes=notes or 'Разовое занятие',
            created_by=created_by,
        )
    return sl


def get_week_grid() -> dict[int, list[ScheduleSlot]]:
    """Расписание по дням недели 0–6."""
    grid = {i: [] for i in range(7)}
    slots = (
        ScheduleSlot.objects.filter(is_archived=False)
        .select_related('direction', 'teacher', 'classroom', 'student')
        .order_by('sort_order', 'start_time')
    )
    for slot in slots:
        grid[slot.day_of_week].append(slot)
    return grid
