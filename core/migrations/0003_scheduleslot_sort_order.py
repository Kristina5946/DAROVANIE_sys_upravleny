# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_direction_lesson_type_and_prices'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduleslot',
            name='sort_order',
            field=models.PositiveIntegerField(default=0, verbose_name='Порядок'),
        ),
        migrations.AlterModelOptions(
            name='scheduleslot',
            options={
                'ordering': ['day_of_week', 'sort_order', 'start_time'],
                'verbose_name': 'Слот расписания',
                'verbose_name_plural': 'Расписание',
            },
        ),
    ]
