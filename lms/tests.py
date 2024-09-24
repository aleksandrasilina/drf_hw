from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User


class CourseTestCase(APITestCase):
    def setUp(self):
        # создаем админа
        self.admin_user = User.objects.create(email="admin@email.com", is_staff=True)

        # создаем модератора
        self.moderator_user = User.objects.create(email="moderator_user@email.com")
        moderators_group, created = Group.objects.get_or_create(name="moderator")
        self.moderator_user.groups.add(moderators_group)

        # создаем обычного пользователя
        self.regular_user = User.objects.create(email="regular_user@email.com")

        # создаем владельца курса и урока
        self.owner_user = User.objects.create(email="owner_user@email.com")

        self.course = Course.objects.create(title="Python", owner=self.owner_user)
        self.lesson = Lesson.objects.create(
            title="DRF", course=self.course, owner=self.owner_user
        )

    # Тесты для админа
    def test_course_retrieve_admin_access(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.course.title)

    def test_course_create_admin_access(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("lms:course-list")
        data = {"title": "Java"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update_admin_access(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("lms:course-detail", args=(self.course.pk,))
        data = {"title": "QA"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "QA")

    def test_course_delete_admin_access(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list_admin_access(self):
        self.client.force_authenticate(user=self.admin_user)
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
                    "lessons": [self.lesson.title],
                    "owner": self.owner_user.pk,
                    'subscription': None
                },
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    # Тесты для модератора
    def test_course_retrieve_moderator_access(self):
        self.client.force_authenticate(user=self.moderator_user)
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.course.title)

    def test_course_create_moderator_access(self):
        self.client.force_authenticate(user=self.moderator_user)
        url = reverse("lms:course-list")
        data = {"title": "Java"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_update_moderator_access(self):
        self.client.force_authenticate(user=self.moderator_user)
        url = reverse("lms:course-detail", args=(self.course.pk,))
        data = {"title": "QA"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "QA")

    def test_course_delete_moderator_access(self):
        self.client.force_authenticate(user=self.moderator_user)
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_list_moderator_access(self):
        self.client.force_authenticate(user=self.moderator_user)
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
                    "lessons": [self.lesson.title],
                    "owner": self.owner_user.pk,
                    'subscription': None
                },
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    # Тесты для обычного пользователя
    def test_course_retrieve_regular_access(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_create_regular_access(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse("lms:course-list")
        data = {"title": "Java"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update_regular_access(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse("lms:course-detail", args=(self.course.pk,))
        data = {"title": "QA"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_delete_regular_access(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_list_regular_access(self):
        self.client.force_authenticate(user=self.regular_user)
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
                    "lessons": [self.lesson.title],
                    "owner": self.owner_user.pk,
                    'subscription': None
                },
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    # Тесты для анонимного пользователя
    def test_course_retrieve_anonymous_access(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_course_create_anonymous_access(self):
        url = reverse("lms:course-list")
        data = {"title": "Java"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_course_update_anonymous_access(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        data = {"title": "QA"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_course_delete_anonymous_access(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_course_list_anonymous_access(self):
        url = reverse("lms:course-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Тесты для владельца курса
    def test_course_retrieve_owner_access(self):
        self.client.force_authenticate(user=self.owner_user)
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.course.title)

    def test_course_create_owner_access(self):
        self.client.force_authenticate(user=self.owner_user)
        url = reverse("lms:course-list")
        data = {"title": "Java"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update_owner_access(self):
        self.client.force_authenticate(user=self.owner_user)
        url = reverse("lms:course-detail", args=(self.course.pk,))
        data = {"title": "QA"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "QA")

    def test_course_delete_owner_access(self):
        self.client.force_authenticate(user=self.owner_user)
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list_owner_access(self):
        self.client.force_authenticate(user=self.owner_user)
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
                    "lessons": [self.lesson.title],
                    "owner": self.owner_user.pk,
                    'subscription': None
                },
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class LessonTestCase(APITestCase):
    def setUp(self):
        # создаем админа
        self.admin_user = User.objects.create(email="admin@email.com", is_staff=True)

        # создаем модератора
        self.moderator_user = User.objects.create(email="moderator_user@email.com")
        moderators_group, created = Group.objects.get_or_create(name="moderator")
        self.moderator_user.groups.add(moderators_group)

        # создаем обычного пользователя
        self.regular_user = User.objects.create(email="regular_user@email.com")

        # создаем владельца курса и урока
        self.owner_user = User.objects.create(email="owner_user@email.com")

        self.course = Course.objects.create(title="Python", owner=self.owner_user)
        self.lesson = Lesson.objects.create(
            title="DRF", course=self.course, owner=self.owner_user
        )

    # Тесты для админа
    def test_lesson_retrieve_admin_access(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("lms:lessons-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create_admin_access(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("lms:lessons-create")
        data = {"title": "Django", "course": self.course.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_wrong_create_admin_access(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("lms:lessons-create")
        data = {
            "title": "Django",
            "course": self.course.pk,
            "video_link": "https://rutube.ru/377/",
        }
        response = self.client.post(url, data)

        self.assertRaises(ValidationError)

    def test_lesson_update_admin_access(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("lms:lessons-update", args=(self.lesson.pk,))
        data = {"title": "Databases"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Databases")

    def test_lesson_delete_admin_access(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("lms:lessons-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list_admin_access(self):
        self.client.force_authenticate(user=self.admin_user)
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
                    "owner": self.owner_user.pk,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    # Тесты для модератора
    def test_lesson_retrieve_moderator_access(self):
        self.client.force_authenticate(user=self.moderator_user)
        url = reverse("lms:lessons-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create_moderator_access(self):
        self.client.force_authenticate(user=self.moderator_user)
        url = reverse("lms:lessons-create")
        data = {"title": "Django", "course": self.course.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_wrong_create_moderator_access(self):
        self.client.force_authenticate(user=self.moderator_user)
        url = reverse("lms:lessons-create")
        data = {
            "title": "Django",
            "course": self.course.pk,
            "video_link": "https://rutube.ru/377/",
        }
        response = self.client.post(url, data)

        self.assertRaises(ValidationError)

    def test_lesson_update_moderator_access(self):
        self.client.force_authenticate(user=self.moderator_user)
        url = reverse("lms:lessons-update", args=(self.lesson.pk,))
        data = {"title": "Databases"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Databases")

    def test_lesson_delete_moderator_access(self):
        self.client.force_authenticate(user=self.moderator_user)
        url = reverse("lms:lessons-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_list_moderator_access(self):
        self.client.force_authenticate(user=self.moderator_user)
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
                    "owner": self.owner_user.pk,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    # Тесты для обычного пользователя
    def test_lesson_retrieve_regular_access(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse("lms:lessons-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_create_regular_access(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse("lms:lessons-create")
        data = {"title": "Django", "course": self.course.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_wrong_create_regular_access(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse("lms:lessons-create")
        data = {
            "title": "Django",
            "course": self.course.pk,
            "video_link": "https://rutube.ru/377/",
        }
        response = self.client.post(url, data)

        self.assertRaises(ValidationError)

    def test_lesson_update_regular_access(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse("lms:lessons-update", args=(self.lesson.pk,))
        data = {"title": "Databases"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_delete_regular_access(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse("lms:lessons-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_list_regular_access(self):
        self.client.force_authenticate(user=self.regular_user)
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
                    "owner": self.owner_user.pk,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    # Тесты для анонимного пользователя
    def test_lesson_retrieve_anonymous_access(self):
        url = reverse("lms:lessons-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_lesson_create_anonymous_access(self):
        url = reverse("lms:lessons-create")
        data = {"title": "Django", "course": self.course.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_wrong_create_anonymous_access(self):
        url = reverse("lms:lessons-create")
        data = {
            "title": "Django",
            "course": self.course.pk,
            "video_link": "https://rutube.ru/377/",
        }
        response = self.client.post(url, data)

        self.assertRaises(ValidationError)

    def test_lesson_update_anonymous_access(self):
        url = reverse("lms:lessons-update", args=(self.lesson.pk,))
        data = {"title": "Databases"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_delete_anonymous_access(self):
        url = reverse("lms:lessons-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_list_anonymous_access(self):
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
                    "owner": self.owner_user.pk,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Тесты для владельца курса
    def test_lesson_retrieve_owner_access(self):
        self.client.force_authenticate(user=self.owner_user)
        url = reverse("lms:lessons-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create_owner_access(self):
        self.client.force_authenticate(user=self.owner_user)
        url = reverse("lms:lessons-create")
        data = {"title": "Django", "course": self.course.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_wrong_create_owner_access(self):
        self.client.force_authenticate(user=self.owner_user)
        url = reverse("lms:lessons-create")
        data = {
            "title": "Django",
            "course": self.course.pk,
            "video_link": "https://rutube.ru/377/",
        }
        response = self.client.post(url, data)

        self.assertRaises(ValidationError)

    def test_lesson_update_owner_access(self):
        self.client.force_authenticate(user=self.owner_user)
        url = reverse("lms:lessons-update", args=(self.lesson.pk,))
        data = {"title": "Databases"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Databases")

    def test_lesson_delete_owner_access(self):
        self.client.force_authenticate(user=self.owner_user)
        url = reverse("lms:lessons-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list_owner_access(self):
        self.client.force_authenticate(user=self.owner_user)
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
                    "owner": self.owner_user.pk,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)