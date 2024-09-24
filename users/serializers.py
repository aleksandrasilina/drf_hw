from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import Payment, User
from users.services import get_stripe_status


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone_number",
            "city",
            "password",
        )


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        exclude = ("payment_status",)


class PaymentRetrieveSerializer(ModelSerializer):
    payment_status = serializers.SerializerMethodField(read_only=True)

    def get_payment_status(self, payment):
        payment.payment_status = get_stripe_status(payment.session_id)
        payment.save()
        return payment.payment_status

    class Meta:
        model = Payment
        fields = "__all__"


class UserDetailSerializer(ModelSerializer):
    payments = PaymentSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "password", "payments")
