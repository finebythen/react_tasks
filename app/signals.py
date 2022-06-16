from django.core.mail import send_mail
from django.db.models import signals
from django.dispatch import receiver
from .models import MainTask, SubTask
from .tasks import mail_new_subtask


@receiver(signals.post_save, sender=MainTask)
def send_request_mail_after_create_maintask(sender, created, instance, **kwargs):
    if created:
        send_mail(
            f'MainTask "{instance.title}" erstellt',
            f'Es wurde ein neuer MainTask mit dem Title {instance.title} erstellt.',
            'django-tasks@email.com',
            ['fmt.api.dummies@gmail.com'],
            fail_silently=False,
        )


@receiver(signals.post_save, sender=SubTask)
def send_request_mail_after_create_subtask(sender, created, instance, **kwargs):
    if created:
        data = {
            'title': instance.title,
        }
        mail_new_subtask.delay(data)