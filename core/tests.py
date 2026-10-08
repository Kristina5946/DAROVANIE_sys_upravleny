from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.models import AttendanceRecord, Direction, ScheduleException, ScheduleSlot, Student, Teacher
from core.services.schedule_day import assign_attendance_teacher, get_lessons_for_date
from core.services.teacher_stats import get_teacher_report


class TeacherSalaryReportTests(TestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(name='Преподаватель')
        self.direction = Direction.objects.create(
            name='Рисование', price_per_lesson=Decimal('1000'),
        )
        self.student = Student.objects.create(name='Ученик')
        self.slot = ScheduleSlot.objects.create(
            direction=self.direction,
            teacher=self.teacher,
            day_of_week=0,
            start_time='10:00',
            end_time='11:00',
        )

    def test_salary_uses_only_paid_present_attendance(self):
        lesson_date = timezone.localdate()
        for present, paid in ((True, True), (True, False), (False, True), (False, False)):
            AttendanceRecord.objects.create(
                student=self.student,
                lesson_date=lesson_date,
                schedule_slot=self.slot,
                direction=self.direction,
                teacher=self.teacher,
                present=present,
                paid=paid,
            )

        report = get_teacher_report(self.teacher, lesson_date, lesson_date)

        self.assertEqual(report['total_visits'], 1)
        self.assertEqual(report['total_revenue'], Decimal('1000'))
        self.assertEqual(report['total_at_percent'], Decimal('300.00'))


class ScheduleHistoryTests(TestCase):
    def test_archived_slot_is_shown_on_its_historical_date(self):
        yesterday = timezone.localdate() - timedelta(days=1)
        direction = Direction.objects.create(name='Музыка')
        student = Student.objects.create(name='Ученик')
        direction.students.add(student)
        slot = ScheduleSlot.objects.create(
            direction=direction,
            day_of_week=yesterday.weekday(),
            start_time='10:00',
            end_time='11:00',
            effective_from=yesterday,
        )
        slot.delete()

        historical_lessons = get_lessons_for_date(yesterday)
        future_same_weekday_lessons = get_lessons_for_date(yesterday + timedelta(days=7))

        self.assertIn(slot.id, [lesson.schedule_slot.id for lesson in historical_lessons])
        self.assertNotIn(slot.id, [lesson.schedule_slot.id for lesson in future_same_weekday_lessons])


class AttendanceTeacherAssignmentTests(TestCase):
    def test_assignment_updates_the_entire_lesson_and_salary(self):
        old_teacher = Teacher.objects.create(name='Предыдущий преподаватель')
        actual_teacher = Teacher.objects.create(name='Фактический преподаватель')
        direction = Direction.objects.create(name='Подготовка')
        first_student = Student.objects.create(name='Первый ученик')
        second_student = Student.objects.create(name='Второй ученик')
        slot = ScheduleSlot.objects.create(
            direction=direction,
            teacher=old_teacher,
            day_of_week=0,
            start_time='10:00',
            end_time='11:00',
        )
        lesson_date = timezone.localdate()
        first_record = AttendanceRecord.objects.create(
            student=first_student,
            lesson_date=lesson_date,
            schedule_slot=slot,
            direction=direction,
            teacher=old_teacher,
            present=True,
            paid=True,
        )
        second_record = AttendanceRecord.objects.create(
            student=second_student,
            lesson_date=lesson_date,
            schedule_slot=slot,
            direction=direction,
            teacher=old_teacher,
            present=True,
            paid=True,
        )

        assign_attendance_teacher(first_record, actual_teacher)

        self.assertEqual(
            list(AttendanceRecord.objects.filter(schedule_slot=slot).values_list('teacher_id', flat=True)),
            [actual_teacher.id, actual_teacher.id],
        )
        self.assertTrue(ScheduleException.objects.filter(
            schedule_slot=slot,
            lesson_date=lesson_date,
            substitute_teacher=actual_teacher,
        ).exists())
        self.assertEqual(get_teacher_report(old_teacher, lesson_date, lesson_date)['total_visits'], 0)
        self.assertEqual(get_teacher_report(actual_teacher, lesson_date, lesson_date)['total_visits'], 2)

    def test_student_attendance_editor_filters_and_updates_teacher(self):
        old_teacher = Teacher.objects.create(name='Первый преподаватель')
        actual_teacher = Teacher.objects.create(name='Второй преподаватель')
        direction = Direction.objects.create(name='Чтение')
        student = Student.objects.create(name='Ученик')
        slot = ScheduleSlot.objects.create(
            direction=direction,
            teacher=old_teacher,
            day_of_week=0,
            start_time='10:00',
            end_time='11:00',
        )
        lesson_date = timezone.localdate()
        record = AttendanceRecord.objects.create(
            student=student,
            lesson_date=lesson_date,
            schedule_slot=slot,
            direction=direction,
            teacher=old_teacher,
            present=True,
            paid=True,
            note='Абонемент',
        )
        user = get_user_model().objects.create_user(username='editor', password='secret')
        self.client.force_login(user)
        url = reverse('core:student_detail', kwargs={'pk': student.pk})

        response = self.client.get(url, {
            'tab': 'attendance',
            'attendance_teacher': old_teacher.pk,
            'attendance_note': 'абон',
        })

        self.assertContains(response, 'Преподаватель')
        self.assertEqual(list(response.context['attendance']), [record])

        response = self.client.post(url + '?tab=attendance&attendance_paid=1', {
            'action': 'save_attendance',
            f'att_present_{record.pk}': 'on',
            f'att_paid_{record.pk}': 'on',
            f'att_teacher_{record.pk}': str(actual_teacher.pk),
            f'att_note_{record.pk}': 'Абонемент',
        })

        self.assertRedirects(response, url + '?tab=attendance&attendance_paid=1')
        record.refresh_from_db()
        self.assertEqual(record.teacher, actual_teacher)

    def test_student_attendance_defaults_to_current_month_and_paginates(self):
        teacher = Teacher.objects.create(name='Преподаватель')
        direction = Direction.objects.create(name='Математика')
        student = Student.objects.create(name='Ученик')
        slot = ScheduleSlot.objects.create(
            direction=direction,
            teacher=teacher,
            day_of_week=0,
            start_time='10:00',
            end_time='11:00',
        )
        for _ in range(31):
            AttendanceRecord.objects.create(
                student=student,
                lesson_date=timezone.localdate(),
                schedule_slot=slot,
                direction=direction,
                teacher=teacher,
            )
        user = get_user_model().objects.create_user(username='viewer', password='secret')
        self.client.force_login(user)
        url = reverse('core:student_detail', kwargs={'pk': student.pk})

        response = self.client.get(url, {'tab': 'attendance'})

        self.assertContains(response, f'value="{timezone.localdate().replace(day=1):%Y-%m-%d}"')
        self.assertEqual(response.context['attendance'].number, 1)
        self.assertEqual(len(response.context['attendance'].object_list), 30)

        response = self.client.get(url, {'tab': 'attendance', 'attendance_page': 2})

        self.assertEqual(response.context['attendance'].number, 2)
        self.assertEqual(len(response.context['attendance'].object_list), 1)
