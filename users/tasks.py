from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def check_last_login():
    """Проверяет пользователей по дате последнего входа и блокирует их, если не заходили более месяца."""

    users = User.objects.all()
    for user in users:
        if user.last_login:
            if user.last_login < timezone.now() - timedelta(days=30):
                user.is_active = False
                user.save()
        else:
            if user.date_joined < timezone.now() - timedelta(days=30):
                user.is_active = False
                user.save()
