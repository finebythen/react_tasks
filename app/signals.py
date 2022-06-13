from django.core.mail import send_mail
from django.db.models import signals
from django.dispatch import receiver
from .models import MainTask, SubTask


@receiver(signals.post_save, sender=MainTask)
def send_request_mail_after_create(sender, created, instance, **kwargs):
    if created:
        send_mail(
            f'MainTask "{instance.title}" erstellt',
            f'Es wurde ein neuer MainTask mit dem Title {instance.title} erstellt.',
            'django-tasks@email.com',
            ['fmt.api.dummies@gmail.com'],
            fail_silently=False,
        )