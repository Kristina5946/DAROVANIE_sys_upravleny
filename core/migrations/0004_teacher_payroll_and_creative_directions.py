# Generated manually

from decimal import Decimal

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_scheduleslot_sort_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='direction',
            name='is_creative',
            field=models.BooleanField(
                default=False,
                help_text='Для расчёта ЗП: вычет с каждого абонемента',
                verbose_name='Творческое направление',
            ),
        ),
        migrations.AddField(
            model_name='direction',
            name='payroll_deduction',
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal('600'),
                help_text='Сумма, вычитаемая из ЗП преподавателя за каждую оплату абонемента',
                max_digits=10,
                verbose_name='Вычет с абонемента (ЗП)',
            ),
        ),
        migrations.AddField(
            model_name='teacher',
            name='manual_bonus',
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal('0'),
                help_text='Доплата к ЗП (можно переопределить за период)',
                max_digits=10,
                verbose_name='Бонус по умолчанию',
            ),
        ),
        migrations.AddField(
            model_name='teacher',
            name='revenue_percent',
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal('30'),
                help_text='Доля от суммы (посещения × цена), %',
                max_digits=5,
                verbose_name='Процент от посещений',
            ),
        ),
        migrations.CreateModel(
            name='TeacherPayrollPeriod',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_from', models.DateField(verbose_name='Период с')),
                ('date_to', models.DateField(verbose_name='Период по')),
                ('revenue_percent', models.DecimalField(decimal_places=2, default=Decimal('30'), max_digits=5, verbose_name='Процент от посещений')),
                ('manual_bonus', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10, verbose_name='Бонус')),
                ('deduct_directions', models.ManyToManyField(blank=True, help_text='Творческие направления: вычет за каждую оплату абонемента', related_name='payroll_deduction_teachers', to='core.direction', verbose_name='Вычет с абонементов по направлениям')),
                ('teacher', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='payroll_periods', to='core.teacher')),
            ],
            options={
                'verbose_name': 'Расчёт ЗП за период',
                'verbose_name_plural': 'Расчёты ЗП за период',
                'ordering': ['-date_from'],
                'unique_together': {('teacher', 'date_from', 'date_to')},
            },
        ),
    ]
