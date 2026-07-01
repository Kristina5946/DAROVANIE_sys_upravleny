# Generated manually for direction refactor

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='direction',
            name='lesson_type',
            field=models.CharField(
                choices=[('group', 'Групповое'), ('individual', 'Индивидуальное')],
                default='group',
                max_length=20,
                verbose_name='Формат',
            ),
        ),
        migrations.AddField(
            model_name='direction',
            name='price_per_lesson',
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal('0'),
                help_text='Стоимость одного занятия при покупке абонемента',
                max_digits=10,
                verbose_name='Цена за занятие (абонемент)',
            ),
        ),
        migrations.RenameField(
            model_name='direction',
            old_name='trial_cost',
            new_name='single_lesson_cost',
        ),
        migrations.AlterField(
            model_name='direction',
            name='description',
            field=models.TextField(blank=True, verbose_name='Краткое описание'),
        ),
        migrations.AlterField(
            model_name='direction',
            name='single_lesson_cost',
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal('500'),
                max_digits=10,
                verbose_name='Цена разового занятия',
            ),
        ),
        migrations.AlterField(
            model_name='direction',
            name='subscription_cost',
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal('0'),
                help_text='Ориентировочная стоимость абонемента на месяц',
                max_digits=10,
                verbose_name='Абонемент (месяц)',
            ),
        ),
        migrations.RemoveField(
            model_name='student',
            name='subdirections',
        ),
    ]
