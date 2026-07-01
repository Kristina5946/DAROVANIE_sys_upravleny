"""
Заполнение БД демо-данными: по 10 записей в основных таблицах.
Использование: python manage.py seed_demo_data [--clear]
"""
from datetime import date, time, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from core.models import (
    AttendanceRecord,
    AuditLog,
    Classroom,
    Direction,
    KanbanTask,
    KanbanStatus,
    LessonType,
    MaterialPurchase,
    NewsItem,
    Parent,
    Payment,
    PaymentType,
    ScheduleSlot,
    SingleLesson,
    SingleLessonType,
    Student,
    Subscription,
    SubscriptionStatus,
    Teacher,
    WeekDay,
)
from core.services.schedule import month_bounds
from core.services.subscriptions import create_custom_subscription

User = get_user_model()

DIRECTIONS = [
    ('Занимательный английский', 'group', 'Игровой английский для детей 4–10 лет', 550, 800, 4400),
    ('Танцевальная студия «Грация»', 'group', 'Классическая и эстрадная хореография', 600, 900, 4800),
    ('Шахматный клуб', 'group', 'Развитие логики и стратегического мышления', 500, 700, 4000),
    ('Программирование', 'group', 'Scratch и Python для школьников', 650, 950, 5200),
    ('Вокальная студия', 'group', 'Постановка голоса, ансамбль', 580, 850, 4640),
    ('Гитара (индивид.)', 'individual', 'Индивидуальные уроки гитары', 1200, 1500, 9600),
    ('Английский (индивид.)', 'individual', 'Персональные занятия с носителем методики', 1400, 1800, 11200),
    ('Подготовка к школе', 'group', 'Развивающие занятия для будущих первоклассников', 480, 650, 3840),
    ('Студия рисования', 'group', 'Живопись, графика, творческие мастер-классы', 700, 750, 2800),
    ('Математика (индивид.)', 'individual', 'Индивидуальная помощь по школьной программе', 1300, 1600, 10400),
]

FIRST_NAMES = [
    'Алиса', 'Давид', 'Есения', 'Марк', 'София',
    'Артём', 'Варвара', 'Илья', 'Милана', 'Тимофей',
]
PARENT_NAMES = [
    'Иванова Мария', 'Петров Сергей', 'Сидорова Анна', 'Козлов Дмитрий', 'Новикова Елена',
    'Морозов Андрей', 'Волкова Ольга', 'Соколов Игорь', 'Лебедева Татьяна', 'Кузнецов Павел',
]
PHONES = [f'+7900{1000000 + i}' for i in range(10)]
TEACHER_NAMES = [
    'Ольга Викторовна', 'Екатерина Сергеевна', 'Анна Михайловна', 'Дмитрий Александрович',
    'Марина Петровна', 'Ирина Николаевна', 'Светлана Юрьевна', 'Алексей Владимирович',
    'Наталья Игоревна', 'Полина Андреевна',
]


class Command(BaseCommand):
    help = 'Заполняет базу демо-данными (по 10 записей в таблицах)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Удалить демо-данные core перед заполнением',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['clear']:
            self._clear()
        if Direction.objects.exists():
            self.stdout.write(self.style.WARNING('Данные уже есть. Используйте --clear для перезаполнения.'))
            return

        today = date.today()
        month_start, month_end = month_bounds(today.year, today.month)

        # Направления
        directions = []
        for name, ltype, desc, ppl, single, sub in DIRECTIONS:
            directions.append(Direction.objects.create(
                name=name,
                lesson_type=ltype,
                description=desc,
                price_per_lesson=Decimal(ppl),
                single_lesson_cost=Decimal(single),
                subscription_cost=Decimal(sub),
                min_age=4 if ltype == 'group' else 6,
                max_age=14 if 'индивид' not in name.lower() else 17,
            ))

        # Родители
        parents = [
            Parent.objects.create(name=PARENT_NAMES[i], phone=PHONES[i], email=f'parent{i}@mail.ru')
            for i in range(10)
        ]

        # Ученики
        students = []
        for i in range(10):
            s = Student.objects.create(
                name=FIRST_NAMES[i] + ' ' + PARENT_NAMES[i].split()[-1][:1] + '.',
                date_of_birth=date(today.year - 7 - i % 5, 3 + i, 10 + i),
                gender='girl' if i % 2 == 0 else 'boy',
                parent=parents[i],
                registration_date=today - timedelta(days=30 * (i + 1)),
                notes=f'Демо-ученик #{i + 1}',
            )
            s.directions.add(directions[i % 10], directions[(i + 3) % 10])
            students.append(s)

        # Преподаватели
        teachers = []
        for i, tname in enumerate(TEACHER_NAMES):
            t = Teacher.objects.create(
                name=tname,
                phone=PHONES[i],
                email=f'teacher{i}@darovanie.ru',
                hire_date=today - timedelta(days=365 * 2 + i * 30),
            )
            t.directions.add(directions[i % 10], directions[(i + 2) % 10])
            teachers.append(t)

        # Преподаватель #0: творческое + обычное (рисование + английский) для теста ЗП
        lead_teacher = teachers[0]
        lead_teacher.directions.set([directions[0], directions[8], directions[1]])
        lead_teacher.save()

        # Кабинеты
        classrooms = [
            Classroom.objects.create(name=n, capacity=c)
            for n, c in [
                ('Большой зал', 15), ('Малый класс', 8), ('Танцзал', 12),
                ('Кабинет 1', 6), ('Кабинет 2', 6), ('Кабинет 3', 10),
                ('Музыкальный', 8), ('IT-лаборатория', 10), ('Студия', 12), ('Ресепшн', 4),
            ]
        ]

        # Расписание (групповые — все ученики направления, индивид. — конкретный ученик)
        days = [WeekDay.MONDAY, WeekDay.TUESDAY, WeekDay.WEDNESDAY, WeekDay.THURSDAY, WeekDay.FRIDAY]
        for i, d in enumerate(directions):
            slot_kwargs = dict(
                direction=d,
                day_of_week=days[i % 5],
                start_time=time(10 + (i % 4), 0),
                end_time=time(11 + (i % 4), 0),
                teacher=teachers[i % 10],
                classroom=classrooms[i % 10],
            )
            if d.lesson_type == LessonType.INDIVIDUAL:
                slot_kwargs['student'] = students[i % 10]
            ScheduleSlot.objects.create(**slot_kwargs)

        admin_user = User.objects.filter(is_superuser=True).first()

        # Абонементы и оплаты
        for i, student in enumerate(students):
            direction = directions[i % 10]
            lessons = 8 if direction.lesson_type == LessonType.GROUP else 4
            amount = direction.price_per_lesson * lessons
            create_custom_subscription(
                student=student,
                direction=direction,
                payment_date=month_start,
                amount=amount,
                total_lessons=lessons,
                notes='Демо-абонемент',
                created_by=admin_user,
            )
            # Доп. разовая оплата
            Payment.objects.create(
                student=student,
                direction=directions[(i + 1) % 10],
                payment_date=today - timedelta(days=i * 3),
                amount=Decimal(700 + i * 100),
                payment_type=PaymentType.SINGLE if i % 2 else PaymentType.TRIAL,
                notes='Демо-оплата',
                created_by=admin_user,
            )

        # Посещения — отметить часть как present
        records = list(AttendanceRecord.objects.all()[:30])
        for j, rec in enumerate(records):
            rec.present = j % 3 != 0
            rec.save(update_fields=['present', 'updated_at'])

        # Демо ЗП: рисование 2800 / 4 занятия, вычет 600, посещения у ведущего преподавателя
        painting = directions[8]
        painting_slot = ScheduleSlot.objects.filter(direction=painting).first()
        if painting_slot:
            painting_slot.teacher = lead_teacher
            painting_slot.save(update_fields=['teacher', 'updated_at'])
        demo_student = students[0]
        demo_student.directions.add(painting)
        create_custom_subscription(
            student=demo_student,
            direction=painting,
            payment_date=month_start,
            amount=Decimal('2800'),
            total_lessons=4,
            notes='Абонемент рисование 4 занятия',
            created_by=admin_user,
        )
        for i, visit_day in enumerate([today - timedelta(days=n) for n in range(2, -1, -1)]):
            if visit_day < month_start:
                continue
            if painting_slot:
                AttendanceRecord.objects.update_or_create(
                    student=demo_student,
                    lesson_date=visit_day,
                    schedule_slot=painting_slot,
                    defaults={
                        'direction': painting,
                        'present': True,
                        'paid': True,
                        'note': f'Демо посещение #{i + 1}',
                    },
                )
        # Доп. посещения разовыми (если в начале месяца мало дней)
        for i in range(2):
            sl = SingleLesson.objects.create(
                student=demo_student,
                direction=painting,
                teacher=lead_teacher,
                lesson_date=today,
                start_time=time(15 + i, 0),
                end_time=time(15 + i, 45),
                lesson_type=SingleLessonType.SINGLE,
                cost=Decimal('700'),
                notes='Демо для расчёта ЗП',
                created_by=admin_user,
            )
            AttendanceRecord.objects.create(
                student=demo_student,
                lesson_date=today,
                single_lesson=sl,
                direction=painting,
                present=True,
                paid=True,
                note='Демо',
            )

        # Разовые занятия
        for i in range(10):
            SingleLesson.objects.create(
                student=students[i],
                direction=directions[(i + 5) % 10],
                teacher=teachers[i],
                lesson_date=today - timedelta(days=i + 1),
                start_time=time(14, 0),
                end_time=time(14, 45),
                lesson_type=SingleLessonType.SINGLE if i % 2 else SingleLessonType.MAKEUP,
                cost=Decimal(800),
            )

        # Закупки
        for i in range(10):
            MaterialPurchase.objects.create(
                name=f'Материалы #{i + 1}',
                direction=directions[i],
                quantity=5 + i,
                unit_cost=Decimal(200 + i * 20),
                total_cost=Decimal((5 + i) * (200 + i * 20)),
                purchase_date=today - timedelta(days=10 + i),
                supplier=f'Поставщик {i + 1}',
            )

        # Канбан
        statuses = [KanbanStatus.TODO, KanbanStatus.IN_PROGRESS, KanbanStatus.DONE]
        for i in range(10):
            KanbanTask.objects.create(
                title=f'Задача {i + 1}',
                description=f'Демо-задача для центра #{i + 1}',
                status=statuses[i % 3],
                assignee=admin_user,
            )

        # Новости
        for i in range(10):
            NewsItem.objects.create(
                text=f'Новость центра #{i + 1}: открыта запись на направления!',
                published_date=today - timedelta(days=i * 2),
                author=admin_user,
            )

        # Аудит
        for i in range(10):
            AuditLog.objects.create(
                user=admin_user,
                action=f'demo_action_{i}',
                details=f'Демо-запись аудита #{i + 1}',
            )

        self.stdout.write(self.style.SUCCESS(
            f'Готово: {Direction.objects.count()} направлений, '
            f'{Student.objects.count()} учеников, '
            f'{Subscription.objects.count()} абонементов, '
            f'{Payment.objects.count()} оплат.'
        ))

    def _clear(self):
        models_order = [
            AttendanceRecord, Subscription, Payment, SingleLesson,
            ScheduleSlot, MaterialPurchase, KanbanTask, NewsItem, AuditLog,
            Student, Teacher, Parent, Classroom, Direction,
        ]
        for model in models_order:
            model.objects.all().delete()
        self.stdout.write('Демо-данные core удалены.')
