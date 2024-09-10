from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}
PAYMENT_CHOICES = (
    (
        "CASH",
        "наличные",
    ),
    (
        "BANK_TRANSFER",
        "банковский перевод",
    ),
)


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone_number = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        help_text="Укажите телефона",
        **NULLABLE,
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        help_text="Загрузите свой аватар",
        **NULLABLE,
    )
    city = models.CharField(
        max_length=100,
        verbose_name="Город",
        help_text="Укажите город",
        **NULLABLE,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
        related_name="payments",
    )
    payment_date = models.DateField(auto_now_add=True, verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный курс",
        help_text="Укажите оплаченный курс",
        related_name="payments",
        **NULLABLE,
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный урок",
        help_text="Укажите оплаченный урок",
        related_name="payments",
        **NULLABLE,
    )
    amount = models.PositiveIntegerField(
        verbose_name="Сумма оплаты", help_text="Укажите сумму оплаты"
    )
    payment_method = models.CharField(
        max_length=50,
        verbose_name="Метод оплаты",
        help_text="Укажите метод оплаты",
        choices=PAYMENT_CHOICES,
    )
