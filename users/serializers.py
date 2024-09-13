from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


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
        fields = "__all__"


class UserDetailSerializer(ModelSerializer):
    payments = PaymentSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "password", "payments")
