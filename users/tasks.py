from celery import shared_task
from django.core.mail import send_mail

from config import settings


@shared_task
def send_subscription_info(email, course):
    """Отправляет пользователю сообщение с информацией о подписке на курс."""

    send_mail(
        subject="Информация о подписке",
        message=f"Дорогой {email}, вы подписались на курс {course}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )
