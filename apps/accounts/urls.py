from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from apps.accounts.views import LogoutView, TelegramLoginView, SendSMSView, VerifySMSView

app_name = 'accounts'

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('telegram-login/',TelegramLoginView.as_view(), name='telegram_login'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('send-sms/', SendSMSView.as_view(), name='send_sms'),
    path('verify-sms/', VerifySMSView.as_view(), name='verify_sms'),
]