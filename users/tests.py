from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course
from users.models import Payment, Subscription, User


class CourseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@email.com")
        self.client.force_authenticate(user=self.user)

    def test_user_retrieve(self):
        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), self.user.email)

    def test_user_create(self):
        url = reverse("users:user-list")
        data = {"email": "user_1@email.com", "password": 123456}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

    def test_user_update(self):
        url = reverse("users:user-detail", args=(self.user.pk,))
        data = {"email": "user_1@email.com"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), "user_1@email.com")

    def test_user_delete(self):
        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 0)

    def test_user_list(self):
        url = reverse("users:user-list")
        response = self.client.get(url)
        data = response.json()

        result = [
            {
                "id": self.user.pk,
                "email": self.user.email,
                "phone_number": None,
                "city": None,
                "password": "",
            }
        ]
        # [
        # {
        #     "id": self.user.pk,
        #     "email": self.user.email,
        #     "first_name": None,
        #     "last_name": None,
        #     "password": self.user.set_password(self.user.password),
        #     "payments": [
        #         {
        #             "id": 8,
        #             "payment_date": "2024-09-13",
        #             "amount": 22000,
        #             "payment_method": "BANK_TRANSFER",
        #             "user": 11,
        #             "paid_course": None,
        #             "paid_lesson": None
        #         }
        #     ]
        # }]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@email.com")
        self.course = Course.objects.create(title="Python", owner=self.user)
        self.payment = Payment.objects.create(
            user=self.user, paid_course=self.course, amount=50000, payment_method="CASH"
        )
        self.client.force_authenticate(user=self.user)

    def test_payment_create(self):
        url = reverse("users:payments-create")
        data = {
            "user": self.user.pk,
            "paid_course": self.course.pk,
            "amount": "60000",
            "payment_method": "BANK_TRANSFER",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.all().count(), 2)

    def test_payment_list(self):
        url = reverse("users:payments-list")
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "id": self.payment.id,
                "payment_date": self.payment.payment_date.strftime("%Y-%m-%d"),
                "amount": self.payment.amount,
                "payment_method": self.payment.payment_method,
                "user": self.user.pk,
                "paid_course": self.course.pk,
                "paid_lesson": None,
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@email.com")
        self.course = Course.objects.create(title="Python", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribtion_create(self):
        url = reverse("users:subscription")
        data = {
            "course_id": self.course.pk,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.all().count(), 1)

    def test_subscribtion_delete(self):
        url = reverse("users:subscription")
        data = {
            "course_id": self.course.pk,
        }
        Subscription.objects.create(course=self.course, user=self.user)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.all().count(), 0)
