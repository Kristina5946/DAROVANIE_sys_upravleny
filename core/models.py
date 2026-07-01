"""
Модели CRM детского центра.
Структура перенесена из Streamlit-приложения (center_data.json) с исправленной
логикой абонементов: при покупке фиксируется total_lessons и период действия.
"""
import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class WeekDay(models.IntegerChoices):
    MONDAY = 0, 'Понедельник'
    TUESDAY = 1, 'Вторник'
    WEDNESDAY = 2, 'Среда'
    THURSDAY = 3, 'Четверг'
    FRIDAY = 4, 'Пятница'
    SATURDAY = 5, 'Суббота'
    SUNDAY = 6, 'Воскресенье'


class Gender(models.TextChoices):
    ANY = '', 'Любой'
    BOY = 'boy', 'Мальчик'
    GIRL = 'girl', 'Девочка'


class PaymentType(models.TextChoices):
    SUBSCRIPTION = 'subscription', 'Абонемент'
    TRIAL = 'trial', 'Пробное'
    SINGLE = 'single', 'Разовое'
    TRANSFER_DEBIT = 'transfer_debit', 'Перенос (списание)'
    TRANSFER_CREDIT = 'transfer_credit', 'Перенос (зачисление)'
    OTHER = 'other', 'Другое'


class LessonExceptionType(models.TextChoices):
    SUBSTITUTION = 'substitution', 'Замена преподавателя'
    CANCEL = 'cancel', 'Отмена'


class SingleLessonType(models.TextChoices):
    SINGLE = 'single', 'Разовое'
    MAKEUP = 'makeup', 'Отработка'


class SubscriptionStatus(models.TextChoices):
    ACTIVE = 'active', 'Активен'
    EXPIRED = 'expired', 'Завершён'
    CANCELLED = 'cancelled', 'Отменён'


class KanbanStatus(models.TextChoices):
    TODO = 'todo', 'ToDo'
    IN_PROGRESS = 'in_progress', 'InProgress'
    DONE = 'done', 'Done'


class LessonType(models.TextChoices):
    GROUP = 'group', 'Групповое'
    INDIVIDUAL = 'individual', 'Индивидуальное'


class Direction(TimeStampedModel):
    """Направление занятий — групповое или индивидуальное."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Название', max_length=255, unique=True)
    description = models.TextField('Краткое описание', blank=True)
    lesson_type = models.CharField(
        'Формат', max_length=20,
        choices=LessonType.choices, default=LessonType.GROUP,
    )
    price_per_lesson = models.DecimalField(
        'Цена за занятие (абонемент)', max_digits=10, decimal_places=2, default=Decimal('0'),
        help_text='Стоимость одного занятия при покупке абонемента',
    )
    single_lesson_cost = models.DecimalField(
        'Цена разового занятия', max_digits=10, decimal_places=2, default=Decimal('500'),
    )
    subscription_cost = models.DecimalField(
        'Абонемент (месяц)', max_digits=10, decimal_places=2, default=Decimal('0'),
        help_text='Ориентировочная стоимость абонемента на месяц',
    )
    min_age = models.PositiveSmallIntegerField('Мин. возраст', default=3)
    max_age = models.PositiveSmallIntegerField('Макс. возраст', default=12)
    gender = models.CharField(
        'Пол', max_length=10, choices=Gender.choices, blank=True, default=Gender.ANY,
    )

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def lesson_type_label(self):
        return self.get_lesson_type_display()

    # Обратная совместимость
    @property
    def trial_cost(self):
        return self.single_lesson_cost


class SubDirection(TimeStampedModel):
    """Поднаправление для индивидуальных занятий внутри основного."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey(
        Direction, on_delete=models.CASCADE, related_name='subdirections',
        verbose_name='Основное направление',
    )
    name = models.CharField('Название', max_length=255)

    class Meta:
        verbose_name = 'Поднаправление'
        verbose_name_plural = 'Поднаправления'
        unique_together = [('parent', 'name')]
        ordering = ['parent__name', 'name']

    @property
    def display_name(self):
        return f'{self.parent.name} ({self.name})'

    def __str__(self):
        return self.display_name


class Parent(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('ФИО', max_length=255)
    phone = models.CharField('Телефон', max_length=50, blank=True)
    email = models.EmailField('Email', blank=True)

    class Meta:
        verbose_name = 'Родитель'
        verbose_name_plural = 'Родители'

    def __str__(self):
        return self.name


class Student(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('ФИО', max_length=255)
    date_of_birth = models.DateField('Дата рождения', null=True, blank=True)
    gender = models.CharField(
        'Пол', max_length=10,
        choices=[('boy', 'Мальчик'), ('girl', 'Девочка')],
        default='boy',
    )
    parent = models.ForeignKey(
        Parent, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='children', verbose_name='Родитель',
    )
    directions = models.ManyToManyField(
        Direction, blank=True, related_name='students', verbose_name='Направления',
    )
    notes = models.TextField('Заметки', blank=True)
    registration_date = models.DateField('Дата регистрации', default=timezone.localdate)

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'
        ordering = ['name']

    def __str__(self):
        return self.name

    def enrolled_labels(self):
        return list(self.directions.values_list('name', flat=True))


class Teacher(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='teacher_profile',
    )
    name = models.CharField('ФИО', max_length=255)
    phone = models.CharField('Телефон', max_length=50, blank=True)
    email = models.EmailField('Email', blank=True)
    hire_date = models.DateField('Дата приёма', null=True, blank=True)
    notes = models.TextField('Заметки', blank=True)
    directions = models.ManyToManyField(
        Direction, blank=True, related_name='teachers', verbose_name='Направления',
    )

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        ordering = ['name']

    def __str__(self):
        return self.name


class Classroom(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Название', max_length=100)
    capacity = models.PositiveSmallIntegerField('Вместимость', default=10)

    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'

    def __str__(self):
        return self.name


class ScheduleSlot(TimeStampedModel):
    """Регулярное занятие в недельном расписании."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    direction = models.ForeignKey(
        Direction, on_delete=models.CASCADE, related_name='schedule_slots',
    )
    subdirection = models.ForeignKey(
        SubDirection, on_delete=models.CASCADE, null=True, blank=True,
        related_name='schedule_slots',
    )
    day_of_week = models.IntegerField('День недели', choices=WeekDay.choices)
    start_time = models.TimeField('Начало')
    end_time = models.TimeField('Конец')
    teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, related_name='schedule_slots',
    )
    classroom = models.ForeignKey(
        Classroom, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='schedule_slots',
    )
    is_archived = models.BooleanField('В архиве', default=False)
    sort_order = models.PositiveIntegerField('Порядок', default=0)
    student = models.ForeignKey(
        'Student', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='schedule_slots', verbose_name='Ученик',
        help_text='Обязательно для индивидуальных занятий',
    )

    class Meta:
        verbose_name = 'Слот расписания'
        verbose_name_plural = 'Расписание'
        ordering = ['day_of_week', 'sort_order', 'start_time']

    def __str__(self):
        return f'{self.get_day_of_week_display()} {self.start_time} — {self.direction}'


class ScheduleException(TimeStampedModel):
    """Замена или отмена занятия на конкретную дату."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson_date = models.DateField('Дата')
    schedule_slot = models.ForeignKey(
        ScheduleSlot, on_delete=models.CASCADE, related_name='exceptions',
    )
    exception_type = models.CharField(
        max_length=20, choices=LessonExceptionType.choices,
    )
    substitute_teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='substitutions',
    )
    notes = models.CharField(max_length=500, blank=True)

    class Meta:
        verbose_name = 'Исключение в расписании'
        verbose_name_plural = 'Исключения в расписании'
        unique_together = [('lesson_date', 'schedule_slot')]


class SingleLesson(TimeStampedModel):
    """Разовое занятие или отработка."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='single_lessons')
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    lesson_date = models.DateField('Дата')
    start_time = models.TimeField('Начало')
    end_time = models.TimeField('Конец')
    lesson_type = models.CharField(
        max_length=20, choices=SingleLessonType.choices, default=SingleLessonType.SINGLE,
    )
    cost = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text='Сумма при переносе/отработке',
    )
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
    )

    class Meta:
        verbose_name = 'Разовое занятие'
        verbose_name_plural = 'Разовые занятия'
        ordering = ['-lesson_date', 'start_time']


class Payment(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateField('Дата оплаты', default=timezone.localdate)
    amount = models.DecimalField('Сумма', max_digits=10, decimal_places=2)
    payment_type = models.CharField(
        'Тип', max_length=30, choices=PaymentType.choices, default=PaymentType.SUBSCRIPTION,
    )
    notes = models.TextField('Примечание', blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
    )

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'
        ordering = ['-payment_date']


class Subscription(TimeStampedModel):
    """
    Абонемент — ключевая сущность для корректного подсчёта посещений.
    При создании фиксируются: период, количество занятий, сумма.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='subscriptions')
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, related_name='subscriptions')
    payment = models.OneToOneField(
        Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name='subscription',
    )
    start_date = models.DateField('Действует с')
    end_date = models.DateField('Действует по')
    total_lessons = models.PositiveSmallIntegerField(
        'Всего занятий',
        help_text='Заполняется автоматически при покупке по расписанию',
    )
    carried_lessons = models.PositiveSmallIntegerField(
        'Перенесённые занятия', default=0,
        help_text='Занятия, перенесённые с прошлого периода',
    )
    amount = models.DecimalField('Сумма', max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=SubscriptionStatus.choices, default=SubscriptionStatus.ACTIVE,
    )
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Абонемент'
        verbose_name_plural = 'Абонементы'
        ordering = ['-start_date']

    @property
    def lessons_available(self):
        return self.total_lessons + self.carried_lessons

    def lessons_used(self):
        return self.attendance_records.filter(present=True).count()

    def lessons_remaining(self):
        return max(0, self.lessons_available - self.lessons_used())

    def usage_percent(self):
        total = self.lessons_available
        if total == 0:
            return 0
        return min(100, round(self.lessons_used() / total * 100))

    def __str__(self):
        return f'{self.student} — {self.direction} ({self.start_date} — {self.end_date})'


class AttendanceRecord(TimeStampedModel):
    """Посещение: связь ученика с конкретным занятием в дату."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    lesson_date = models.DateField('Дата занятия')
    schedule_slot = models.ForeignKey(
        ScheduleSlot, on_delete=models.CASCADE, null=True, blank=True,
        related_name='attendance_records',
    )
    single_lesson = models.ForeignKey(
        SingleLesson, on_delete=models.CASCADE, null=True, blank=True,
        related_name='attendance_records',
    )
    subscription = models.ForeignKey(
        Subscription, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='attendance_records',
    )
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    present = models.BooleanField('Был', default=False)
    paid = models.BooleanField('Оплачено', default=False)
    note = models.CharField('Примечание', max_length=500, blank=True)

    class Meta:
        verbose_name = 'Посещение'
        verbose_name_plural = 'Посещения'
        ordering = ['-lesson_date']

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.schedule_slot and not self.single_lesson:
            raise ValidationError('Укажите слот расписания или разовое занятие.')
        if self.schedule_slot and self.single_lesson:
            raise ValidationError('Нельзя указать оба типа занятия одновременно.')


class MaterialPurchase(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Название', max_length=255)
    direction = models.ForeignKey(
        Direction, on_delete=models.SET_NULL, null=True, blank=True,
    )
    quantity = models.PositiveIntegerField('Количество', default=1)
    unit_cost = models.DecimalField('Цена за ед.', max_digits=10, decimal_places=2)
    total_cost = models.DecimalField('Итого', max_digits=10, decimal_places=2)
    purchase_date = models.DateField('Дата закупки')
    supplier = models.CharField('Поставщик', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Закупка материалов'
        verbose_name_plural = 'Закупки материалов'


class KanbanTask(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('Заголовок', max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=KanbanStatus.choices, default=KanbanStatus.TODO,
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
    )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Канбан'


class NewsItem(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField('Текст')
    published_date = models.DateField(default=timezone.localdate)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
    )
    image = models.ImageField(upload_to='news/', blank=True, null=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-published_date']


class AuditLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
    )
    action = models.CharField(max_length=100)
    details = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Запись аудита'
        verbose_name_plural = 'Аудит'
        ordering = ['-timestamp']


class CenterSettings(models.Model):
    """Глобальные настройки центра (singleton)."""
    trial_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('500'))
    single_cost_multiplier = models.DecimalField(
        max_digits=4, decimal_places=2, default=Decimal('1.5'),
    )

    class Meta:
        verbose_name = 'Настройки центра'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
