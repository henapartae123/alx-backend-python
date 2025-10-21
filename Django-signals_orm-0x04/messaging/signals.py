from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification


@receiver(post_save, sender=Message)
def create_notification_for_message(sender, instance, created, **kwargs):
    """
    Triggered when a new Message instance is created.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )
