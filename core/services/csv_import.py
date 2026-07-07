"""
Импорт учеников и преподавателей из CSV старого приложения (Streamlit).
"""
import csv
import re
from datetime import datetime
from pathlib import Path

from django.db import transaction
from django.utils import timezone

from core.models import Direction, LessonType, Parent, Student, Teacher

INDIVIDUAL_KEYWORDS = ('индивидуальн', 'индивидуально')


def _clean(value) -> str:
    if value is None:
        return ''
    text = str(value).strip()
    if text.lower() in ('nan', 'none', ''):
        return ''
    return text


def _parse_bool(value) -> bool:
    text = _clean(value).lower()
    return text in ('true', '1', 'да', 'yes')


def _parse_date(value):
    text = _clean(value)
    if not text:
        return None
    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y'):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def _parse_gender(value) -> str:
    text = _clean(value).lower()
    if 'девоч' in text or text == 'girl':
        return 'girl'
    return 'boy'


def _split_directions(raw: str) -> list[str]:
    raw = _clean(raw)
    if not raw:
        return []
    # Направления в CSV разделены запятой; внутри названия бывает «(2, 4 класс)»
    parts = re.split(
        r',\s+(?=(?:[А-ЯA-Z"«]|Индивидуальн|индивидуальн|Занимательн|Студия|Танцевальн|'
        r'Вокальн|Логопед|Курс|HIP|Увлекательн|Программирование|Мастерская|Речевая|танцевальн))',
        raw,
    )
    return [p.strip() for p in parts if p.strip()]


def _guess_lesson_type(name: str) -> str:
    lower = name.lower()
    if any(kw in lower for kw in INDIVIDUAL_KEYWORDS):
        return LessonType.INDIVIDUAL
    return LessonType.GROUP


def _normalize_phone(phone: str) -> str:
    return re.sub(r'\s+', ' ', _clean(phone))


def get_or_create_direction(name: str) -> Direction:
    name = _clean(name)
    direction, created = Direction.objects.get_or_create(
        name=name,
        defaults={
            'lesson_type': _guess_lesson_type(name),
            'description': 'Импорт из старой CRM',
        },
    )
    return direction


def _get_parent(parent_name: str, phone: str) -> Parent | None:
    parent_name = _clean(parent_name)
    phone = _normalize_phone(phone)
    if not parent_name and not phone:
        return None
    if not parent_name:
        parent_name = 'Родитель'
    if phone:
        parent = Parent.objects.filter(phone=phone).first()
        if parent:
            if parent_name and parent.name != parent_name:
                parent.name = parent_name
                parent.save(update_fields=['name', 'updated_at'])
            return parent
    return Parent.objects.create(name=parent_name, phone=phone)


def import_teachers_csv(path: Path, *, dry_run: bool = False) -> dict:
    stats = {'created': 0, 'updated': 0, 'directions': 0, 'skipped': 0}
    with path.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = _clean(row.get('name'))
            if not name:
                stats['skipped'] += 1
                continue
            phone = _normalize_phone(row.get('phone', ''))
            email = _clean(row.get('email', ''))
            notes = _clean(row.get('notes', ''))
            direction_names = _split_directions(row.get('directions', ''))

            if dry_run:
                stats['created'] += 1
                stats['directions'] += len(direction_names)
                continue

            teacher, created = Teacher.objects.get_or_create(
                name=name,
                defaults={
                    'phone': phone,
                    'email': email,
                    'notes': notes,
                    'hire_date': timezone.localdate(),
                },
            )
            if created:
                stats['created'] += 1
            else:
                stats['updated'] += 1
                teacher.phone = phone or teacher.phone
                teacher.email = email or teacher.email
                if notes:
                    teacher.notes = notes
                teacher.save()

            directions = []
            for dname in direction_names:
                directions.append(get_or_create_direction(dname))
                stats['directions'] += 1
            if directions:
                teacher.directions.add(*directions)

    return stats


def import_students_csv(path: Path, *, dry_run: bool = False, skip_test: bool = True) -> dict:
    stats = {'created': 0, 'updated': 0, 'directions': 0, 'skipped': 0}

    with path.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Гибкие имена колонок (с эмодзи в заголовках)
            name = _clean(row.get('ФИО Ученика') or row.get('name'))
            if not name:
                stats['skipped'] += 1
                continue
            if skip_test and name.lower() in ('тестовый', 'тест', 'test'):
                stats['skipped'] += 1
                continue

            delete_flag = _parse_bool(
                row.get('🗑️') or row.get('delete') or row.get('Удалить') or ''
            )
            if delete_flag:
                stats['skipped'] += 1
                continue

            dob = _parse_date(row.get('Дата рождения'))
            gender = _parse_gender(row.get('Пол'))
            parent_name = _clean(row.get('ФИО Родителя'))
            phone = _normalize_phone(
                row.get('📞 Телефон(ы)') or row.get('Телефон') or row.get('phone') or ''
            )
            notes = _clean(row.get('Заметки'))
            if notes.lower() == 'nan':
                notes = ''
            direction_names = _split_directions(row.get('Направления', ''))

            if dry_run:
                stats['created'] += 1
                stats['directions'] += len(direction_names)
                continue

            parent = _get_parent(parent_name, phone)
            student, created = Student.objects.get_or_create(
                name=name,
                defaults={
                    'date_of_birth': dob,
                    'gender': gender,
                    'parent': parent,
                    'notes': notes,
                },
            )
            if created:
                stats['created'] += 1
            else:
                stats['updated'] += 1
                if dob:
                    student.date_of_birth = dob
                student.gender = gender
                if parent:
                    student.parent = parent
                if notes:
                    student.notes = notes
                student.save()

            directions = []
            for dname in direction_names:
                directions.append(get_or_create_direction(dname))
                stats['directions'] += 1
            if directions:
                student.directions.add(*directions)

    return stats
