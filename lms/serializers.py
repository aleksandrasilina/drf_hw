from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson
from lms.validators import VideoLinkValidator
from users.models import Subscription


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [VideoLinkValidator(field="video_link")]


class CourseSerializer(ModelSerializer):
    lesson_count = serializers.IntegerField(source="lessons.all.count", read_only=True)
    lessons = SerializerMethodField()
    subscription = SerializerMethodField()

    def get_lessons(self, course):
        return [lesson.title for lesson in Lesson.objects.filter(course=course)]

    def get_subscription(self, course):
        user = self.context.get('request').user
        for subscription in Subscription.objects.filter(user=user, course=course):
            return subscription.is_active

    class Meta:
        model = Course
        fields = ("id", "title", "description", "lesson_count", "lessons", "owner", "subscription")
