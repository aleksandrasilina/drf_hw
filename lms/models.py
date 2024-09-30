from django.db import models

from config import settings

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(
        max_length=100, verbose_name="Курс", help_text="Укажите курс"
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Опишите курс", **NULLABLE
    )
    preview = models.TextField(
        verbose_name="Превью", help_text="Загрузите превью", **NULLABLE
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="courses",
        verbose_name="Владелец",
        help_text="Укажите владельца курса",
        **NULLABLE,
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Обновлено",
        help_text="Укажите дату и время обновления",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(
        max_length=100, verbose_name="Урок", help_text="Укажите урок"
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Опишите урок", **NULLABLE
    )
    preview = models.TextField(
        verbose_name="Превью", help_text="Загрузите превью", **NULLABLE
    )
    video_link = models.URLField(
        verbose_name="Ссылка на видео", help_text="Укажите ссылку на видео", **NULLABLE
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="lessons"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="lessons",
        verbose_name="Владелец",
        help_text="Укажите владельца урока",
        **NULLABLE,
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Обновлено",
        help_text="Укажите дату и время обновления",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
