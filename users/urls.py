from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (PaymentCreateAPIView, PaymentListAPIView,
                         SubscriptionAPIView, UserViewSet)

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", UserViewSet)

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payments-list"),
    path("payments/create/", PaymentCreateAPIView.as_view(), name="payments-create"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("subscription/", SubscriptionAPIView.as_view(), name="subscription"),
]

urlpatterns += router.urls
