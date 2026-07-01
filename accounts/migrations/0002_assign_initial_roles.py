from django.db import migrations


def assign_roles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('accounts', 'UserProfile')
    for user in User.objects.all():
        if UserProfile.objects.filter(user=user).exists():
            continue
        role = 'director' if (user.is_superuser or user.is_staff) else 'reception'
        UserProfile.objects.create(user=user, role=role)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(assign_roles, noop),
    ]
