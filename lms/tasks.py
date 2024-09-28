from celery import shared_task
from django.core.mail import send_mail

from config import settings


@shared_task
def send_update_info(email_list, course):
    """Отправляет пользователю сообщение с информацией об обновлении курса."""

    for user in email_list:
        send_mail(
            subject="Обновление курса",
            message=f"Дорогой {user}, сообщаем вам, что курс {course} обновился",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=email_list,
        )
