"""
Исправление типичных ошибок в данных абонементов:
- отвязка разовых/отработок от абонементов;
- слияние дублирующих абонементов без оплаты;
- установка price_per_lesson для направлений, где он не задан.
"""
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import AttendanceRecord, Direction, Subscription
from core.services.subscriptions import link_attendance_to_active_subscription


class Command(BaseCommand):
    help = 'Исправить привязки посещений и дубли абонементов'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Только показать, что будет изменено',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        if dry_run:
            self.stdout.write(self.style.WARNING('Режим dry-run — изменения не сохраняются'))

        with transaction.atomic():
            unlinked = self._unlink_single_lessons_from_subscriptions(dry_run)
            merged = self._merge_duplicate_subscriptions(dry_run)
            relinked = self._relink_schedule_attendance(dry_run)
            prices = self._fix_direction_prices(dry_run)

            if dry_run:
                transaction.set_rollback(True)

        self.stdout.write(self.style.SUCCESS(
            f'Готово: отвязано разовых={unlinked}, слито дублей={merged}, '
            f'перепривязано={relinked}, цен направлений={prices}'
        ))

    def _unlink_single_lessons_from_subscriptions(self, dry_run: bool) -> int:
        qs = AttendanceRecord.objects.filter(
            single_lesson__isnull=False,
            subscription__isnull=False,
        )
        count = qs.count()
        if count and not dry_run:
            qs.update(subscription=None)
        self.stdout.write(f'Разовые/отработки, отвязанные от абонементов: {count}')
        return count

    def _merge_duplicate_subscriptions(self, dry_run: bool) -> int:
        """Слить пустой дубль (без оплаты) в оплаченный абонемент того же ученика и направления."""
        merged = 0
        paid_subs = Subscription.objects.filter(
            payment__isnull=False,
            status='active',
        ).select_related('student', 'direction', 'payment')

        for paid in paid_subs:
            duplicates = Subscription.objects.filter(
                student=paid.student,
                direction=paid.direction,
                status='active',
                payment__isnull=True,
            ).exclude(pk=paid.pk)
            for dup in duplicates:
                att_count = dup.attendance_records.count()
                self.stdout.write(
                    f'  Merge: {paid.student.name} / {paid.direction.name[:40]} '
                    f'<- dup {dup.pk} ({att_count} attendance)'
                )
                if not dry_run:
                    dup.attendance_records.update(subscription=paid)
                    dup.delete()
                merged += 1
        return merged

    def _relink_schedule_attendance(self, dry_run: bool) -> int:
        relinked = 0
        records = AttendanceRecord.objects.filter(
            schedule_slot__isnull=False,
            single_lesson__isnull=True,
            present=True,
        ).select_related('student', 'direction')
        for record in records:
            old_sub_id = record.subscription_id
            if dry_run:
                continue
            link_attendance_to_active_subscription(record)
            record.refresh_from_db()
            if record.subscription_id != old_sub_id:
                relinked += 1
        self.stdout.write(f'Relinked schedule attendance: {relinked}')
        return relinked

    def _fix_direction_prices(self, dry_run: bool) -> int:
        fixed = 0
        for direction in Direction.objects.all():
            if direction.price_per_lesson and direction.price_per_lesson > 0:
                continue
            if direction.subscription_cost and direction.subscription_cost > 0:
                lessons = 4
                price = (direction.subscription_cost / Decimal(lessons)).quantize(Decimal('0.01'))
            elif direction.single_lesson_cost and direction.single_lesson_cost > 0:
                price = direction.single_lesson_cost
            else:
                continue
            self.stdout.write(f'  {direction.name[:50]}: price_per_lesson = {price}')
            if not dry_run:
                direction.price_per_lesson = price
                direction.save(update_fields=['price_per_lesson', 'updated_at'])
            fixed += 1
        return fixed
