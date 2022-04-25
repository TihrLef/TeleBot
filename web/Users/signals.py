from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User

@receiver(post_save, sender=User)
def default_to_non_active(sender, instance, created, **kwargs):
    if created:
        instance.is_active = False
        instance.save()