from datetime import date
from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()

WEEKDAY_LABELS = {
    0: 'Понедельник', 1: 'Вторник', 2: 'Среда', 3: 'Четверг',
    4: 'Пятница', 5: 'Суббота', 6: 'Воскресенье',
}


@register.filter
def weekday_label(day_num):
    return WEEKDAY_LABELS.get(day_num, '')


@register.filter
def age_years(dob):
    if not dob:
        return '—'
    today = date.today()
    years = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return years


@register.filter
def gender_label(value):
    return {'boy': 'Мальчик', 'girl': 'Девочка'}.get(value, value)


@register.filter
def input_number(value):
    """Значение для HTML input type=number (точка, без локали)."""
    if value is None or value == '':
        return ''
    try:
        d = Decimal(str(value))
    except (InvalidOperation, ValueError):
        return value
    text = format(d, 'f')
    if '.' in text:
        text = text.rstrip('0').rstrip('.')
    return text
