from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def check_last_login():
    """Проверяет пользователей по дате последнего входа и блокирует их, если не заходили более месяца."""

    User.objects.filter(
        last_login__lt=timezone.now() - timedelta(days=30), is_active=True
    ).update(is_active=False)
