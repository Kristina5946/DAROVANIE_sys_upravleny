"""
Импорт учеников и преподавателей из CSV старого приложения.

Использование:
  python manage.py import_legacy_csv
  python manage.py import_legacy_csv --students data/import/students.csv --teachers data/import/teachers.csv
  python manage.py import_legacy_csv --dry-run
"""
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from core.services.csv_import import import_students_csv, import_teachers_csv


class Command(BaseCommand):
    help = 'Импорт учеников и преподавателей из CSV (экспорт старой CRM)'

    def add_arguments(self, parser):
        base = Path(settings.BASE_DIR) / 'data' / 'import'
        parser.add_argument(
            '--students',
            default=str(base / 'students.csv'),
            help='Путь к CSV учеников',
        )
        parser.add_argument(
            '--teachers',
            default=str(base / 'teachers.csv'),
            help='Путь к CSV преподавателей',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Только подсчёт, без записи в БД',
        )
        parser.add_argument(
            '--include-test',
            action='store_true',
            help='Включить тестовых учеников',
        )

    def handle(self, *args, **options):
        students_path = Path(options['students'])
        teachers_path = Path(options['teachers'])
        dry_run = options['dry_run']

        if not teachers_path.exists():
            self.stderr.write(self.style.ERROR(f'Не найден файл: {teachers_path}'))
            return

        if not students_path.exists():
            self.stderr.write(self.style.ERROR(f'Не найден файл: {students_path}'))
            return

        if dry_run:
            self.stdout.write(self.style.WARNING('Режим dry-run — в БД ничего не пишется'))

        self.stdout.write(f'Преподаватели: {teachers_path}')
        if dry_run:
            t_stats = import_teachers_csv(teachers_path, dry_run=True)
        else:
            with transaction.atomic():
                t_stats = import_teachers_csv(teachers_path, dry_run=False)
        self.stdout.write(self.style.SUCCESS(
            f"  создано: {t_stats['created']}, обновлено: {t_stats['updated']}, "
            f"направлений привязано: {t_stats['directions']}, пропущено: {t_stats['skipped']}"
        ))

        self.stdout.write(f'Ученики: {students_path}')
        if dry_run:
            s_stats = import_students_csv(
                students_path,
                dry_run=True,
                skip_test=not options['include_test'],
            )
        else:
            with transaction.atomic():
                s_stats = import_students_csv(
                    students_path,
                    dry_run=False,
                    skip_test=not options['include_test'],
                )
        self.stdout.write(self.style.SUCCESS(
            f"  создано: {s_stats['created']}, обновлено: {s_stats['updated']}, "
            f"направлений привязано: {s_stats['directions']}, пропущено: {s_stats['skipped']}"
        ))

        if not dry_run:
            from core.models import Direction, Student, Teacher
            self.stdout.write(self.style.SUCCESS(
                f'Итого в БД: {Student.objects.count()} учеников, '
                f'{Teacher.objects.count()} преподавателей, '
                f'{Direction.objects.count()} направлений'
            ))
