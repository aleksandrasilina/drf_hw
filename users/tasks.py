from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta

from config import settings
from users.models import User


@shared_task
def send_subscription_info(email, course):
    """Отправляет пользователю сообщение с информацией о подписке на курс."""

    send_mail(
        subject="Информация о подписке",
        message=f"Дорогой {email}, вы подписались на курс {course}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )


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
