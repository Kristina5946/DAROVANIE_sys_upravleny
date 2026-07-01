from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import StaffRole, UserProfile

User = get_user_model()


@receiver(post_save, sender=User)
def ensure_user_profile(sender, instance, created, **kwargs):
    if created:
        role = StaffRole.DIRECTOR if instance.is_superuser else StaffRole.RECEPTION
        UserProfile.objects.get_or_create(user=instance, defaults={'role': role})
