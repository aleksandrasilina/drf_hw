from django.urls import reverse
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User


class CourseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@email.com")
        self.course = Course.objects.create(title="Python", owner=self.user)
        self.lesson = Lesson.objects.create(title="DRF", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.course.title)

    def test_course_create(self):
        url = reverse("lms:course-list")
        data = {
            "title": "Java"
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        data = {
            "title": "QA"
        }
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "QA")

    def test_course_delete(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        url = reverse("lms:course-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "title": self.course.title,
                    "description": None,
                    "lesson_count": 1,
                    "lessons": [
                        self.lesson.title
                    ],
                    "owner": self.user.pk
                },
            ]
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@email.com")
        self.course = Course.objects.create(title="Python", owner=self.user)
        self.lesson = Lesson.objects.create(title="DRF", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("lms:lessons-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        url = reverse("lms:lessons-create")
        data = {
            "title": "Django",
            "course": self.course.pk
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_wrong_create(self):
        url = reverse("lms:lessons-create")
        data = {
            "title": "Django",
            "course": self.course.pk,
            "video_link": "https://rutube.ru/377/"
        }
        response = self.client.post(url, data)

        self.assertRaises(ValidationError)


    def test_lesson_update(self):
        url = (reverse("lms:lessons-update", args=(self.lesson.pk,)))
        data = {
            "title": "Databases"
        }
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Databases")

    def test_lesson_delete(self):
        url = reverse("lms:lessons-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("lms:lessons-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title": self.lesson.title,
                    "description": None,
                    "preview": None,
                    "video_link": None,
                    "course": self.course.pk,
                    "owner": self.user.pk
                }
            ]
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
