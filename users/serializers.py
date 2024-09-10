from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
        )


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserDetailSerializer(ModelSerializer):
    payments = PaymentSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "email", "password", "payments")
