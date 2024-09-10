from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.serializers import (PaymentSerializer, UserDetailSerializer,
                               UserSerializer)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        return UserSerializer


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # , filters.OrderingFilter, filters.SearchFilter
    filterset_fields = ("paid_lesson", "paid_course", "payment_method")
    ordering_fields = ("payment_date",)


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
