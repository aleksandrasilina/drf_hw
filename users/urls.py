from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentCreateAPIView, PaymentListAPIView, UserViewSet

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", UserViewSet)


urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payments_list"),
    path("payments/create/", PaymentCreateAPIView.as_view(), name="payments_create"),

    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
