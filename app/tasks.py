from django.core.mail import send_mail
from proj.celery import app


@app.task
def mail_new_subtask(data):
    send_mail(
        f'SubTask "{data["title"]}" erstellt',
        f'Es wurde ein neuer SubTask mit dem Title {data["title"]} erstellt.',
        'django-tasks@email.com',
        ['fmt.api.dummies@gmail.com'],
        fail_silently=False,
    )