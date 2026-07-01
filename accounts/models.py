from django.conf import settings
from django.db import models


class StaffRole(models.TextChoices):
    DIRECTOR = 'director', 'Директор'
    RECEPTION = 'reception', 'Ресепшн'


class UserProfile(models.Model):
    """Роль сотрудника в CRM (отдельно от is_staff для Django admin)."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь',
    )
    role = models.CharField(
        'Роль в CRM',
        max_length=20,
        choices=StaffRole.choices,
        default=StaffRole.RECEPTION,
    )

    class Meta:
        verbose_name = 'Профиль сотрудника'
        verbose_name_plural = 'Профили сотрудников'

    def __str__(self):
        return f'{self.user.username} — {self.get_role_display()}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.user.is_superuser:
            return
        if self.role == StaffRole.DIRECTOR:
            if not self.user.is_staff:
                self.user.is_staff = True
                self.user.save(update_fields=['is_staff'])
        elif self.role == StaffRole.RECEPTION:
            updates = {}
            if self.user.is_staff:
                updates['is_staff'] = False
            if self.user.is_superuser:
                updates['is_superuser'] = False
            if updates:
                for k, v in updates.items():
                    setattr(self.user, k, v)
                self.user.save(update_fields=list(updates.keys()))
