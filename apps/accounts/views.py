from django.shortcuts import render
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
import hashlib
import hmac
from django.conf import settings
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from apps.accounts.models import User


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user=request.user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)
        return Response({"message": "Logged out successfully"})


def verify_telegram_auth(data):
    """Telegramdan kelgan ma'lumotlarni tekshirish."""
    bot_token = settings.TELEGRAM_BOT_TOKEN
    secret_key = hashlib.sha256(bot_token.encode()).digest()

    auth_data = {k: v for k, v in data.items() if k != 'hash'}
    auth_data_sorted = sorted(auth_data.items())
    data_check_string = "\n".join(f"{k}={v}" for k, v in auth_data_sorted)
    
    hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    return hmac_hash == data.get('hash')

class TelegramLoginAPIView(APIView):
    """Telegram orqali foydalanuvchini autentifikatsiya qilish"""
    permission_classes = [AllowAny]

    def get(self, request):
        data = request.query_params.dict()

        # Ma'lumotlarni tekshiramiz
        if not verify_telegram_auth(data):
            return Response({"error": "Authentication failed"}, status=status.HTTP_400_BAD_REQUEST)

        telegram_user_id = data.get("id")
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")
        username = data.get("username", "")

        # Foydalanuvchini bazada qidiramiz yoki yaratamiz
        user, created = User.objects.get_or_create(
            telegram_user_id=telegram_user_id,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "username": username if username else f"tg-{telegram_user_id}"
            }
        )

        # Foydalanuvchini tizimga kiritamiz
        login(request, user)

        return Response(
            {"message": "Successfully logged in", "user_id": user.id, "username": user.username},
            status=status.HTTP_200_OK
        )
