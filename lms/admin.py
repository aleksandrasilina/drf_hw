from django.contrib import admin

from lms.models import Course


@admin.register(Course)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "updated_at")
