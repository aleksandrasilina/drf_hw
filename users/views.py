from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.tasks import send_subscription_info
from lms.models import Course
from users.models import Payment, Subscription, User
from users.permissions import IsProfileOwner
from users.serializers import (PaymentRetrieveSerializer, PaymentSerializer,
                               UserDetailSerializer, UserSerializer)
from users.services import (create_stripe_price, create_stripe_product,
                            create_stripe_session)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if (
            self.action == "retrieve"
            and self.request.user == User.objects.get(pk=self.kwargs.get("pk"))
            or self.request.user.is_superuser
        ):
            return UserDetailSerializer
        return UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (AllowAny,)
        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = (IsAuthenticated, IsProfileOwner | IsAdminUser)

        return super().get_permissions()


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("paid_lesson", "paid_course", "payment_method")
    ordering_fields = ("payment_date",)


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product = create_stripe_product(
            payment.paid_course if payment.paid_course else payment.paid_lesson
        )
        price = create_stripe_price(product, payment.amount)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.payment_method = "BANK_TRANSFER"
        payment.save()


class PaymentDestroyAPIView(DestroyAPIView):
    queryset = Payment.objects.all()


class PaymentRetrieveAPIView(RetrieveAPIView):
    serializer_class = PaymentRetrieveSerializer
    queryset = Payment.objects.all()


class SubscriptionAPIView(APIView):
    queryset = Subscription.objects.all()

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course_id")
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"

        else:
            Subscription.objects.create(user=user, course=course_item)
            send_subscription_info.delay(user.email, course_item.title)
            message = "Подписка добавлена"
        return Response({"message": message})
