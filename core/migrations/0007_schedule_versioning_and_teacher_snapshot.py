# Generated for fixing schedule history loss — versioning + teacher snapshot.
import django.db.models.deletion
from django.db import migrations, models
import django.db.models


def backfill_teacher_snapshot(apps, schema_editor):
    AttendanceRecord = apps.get_model('core', 'AttendanceRecord')
    ScheduleSlot = apps.get_model('core', 'ScheduleSlot')
    SingleLesson = apps.get_model('core', 'SingleLesson')
    # Заполнить снимок преподавателя из текущего слота/разового занятия
    # Для регулярных — взять teacher из ScheduleSlot
    # Для разовых — из SingleLesson
    qs = AttendanceRecord.objects.select_related('schedule_slot', 'single_lesson').filter(teacher__isnull=True)
    for rec in qs.iterator(chunk_size=500):
        teacher_id = None
        if rec.schedule_slot_id and rec.schedule_slot:
            teacher_id = rec.schedule_slot.teacher_id
        elif rec.single_lesson_id and rec.single_lesson:
            teacher_id = rec.single_lesson.teacher_id
        if teacher_id:
            AttendanceRecord.objects.filter(pk=rec.pk).update(teacher_id=teacher_id)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_schedule_slot_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduleslot',
            name='effective_from',
            field=models.DateField(blank=True, help_text='Пусто — с момента создания. При редактировании создаётся новая версия.', null=True, verbose_name='Действует с'),
        ),
        migrations.AddField(
            model_name='scheduleslot',
            name='effective_to',
            field=models.DateField(blank=True, help_text='Пусто — бессрочно. При удалении/изменении ставится вчера.', null=True, verbose_name='Действует по'),
        ),
        migrations.AddField(
            model_name='attendancerecord',
            name='teacher',
            field=models.ForeignKey(blank=True, help_text='Фиксируется при создании посещения, не меняется при редактировании слота', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attendance_snapshots', to='core.teacher', verbose_name='Преподаватель (снимок)'),
        ),
        migrations.AlterField(
            model_name='attendancerecord',
            name='schedule_slot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attendance_records', to='core.scheduleslot'),
        ),
        migrations.RunPython(backfill_teacher_snapshot, migrations.RunPython.noop),
    ]
