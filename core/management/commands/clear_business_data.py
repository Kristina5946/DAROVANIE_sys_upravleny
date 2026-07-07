"""
Очистка бизнес-данных CRM (ученики, оплаты, расписание и т.д.).
Пользователи Django (логины) сохраняются.

Использование: python manage.py clear_business_data
               python manage.py clear_business_data --yes
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import (
    AttendanceRecord,
    AuditLog,
    Classroom,
    Direction,
    KanbanTask,
    MaterialPurchase,
    NewsItem,
    Parent,
    Payment,
    ScheduleException,
    ScheduleSlot,
    SingleLesson,
    Student,
    SubDirection,
    Subscription,
    Teacher,
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Удалить все данные CRM, оставить пользователей и миграции'

    def add_arguments(self, parser):
        parser.add_argument(
            '--yes',
            action='store_true',
            help='Не спрашивать подтверждение',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if not options['yes']:
            self.stdout.write(self.style.WARNING(
                'Будут удалены: ученики, преподаватели, оплаты, расписание, абонементы и пр.'
            ))
            self.stdout.write('Пользователи (admin и др.) останутся.')
            confirm = input('Продолжить? [y/N]: ').strip().lower()
            if confirm not in ('y', 'yes', 'д', 'да'):
                self.stdout.write('Отменено.')
                return

        models_order = [
            AttendanceRecord,
            Subscription,
            Payment,
            SingleLesson,
            ScheduleException,
            ScheduleSlot,
            MaterialPurchase,
            KanbanTask,
            NewsItem,
            AuditLog,
            Student,
            Teacher,
            Parent,
            Classroom,
            SubDirection,
            Direction,
        ]
        totals = {}
        for model in models_order:
            count, _ = model.objects.all().delete()
            totals[model._meta.label] = count

        users_count = User.objects.count()
        self.stdout.write(self.style.SUCCESS('База очищена от рабочих данных.'))
        for label, count in totals.items():
            if count:
                self.stdout.write(f'  {label}: {count}')
        self.stdout.write(f'Пользователей сохранено: {users_count}')
