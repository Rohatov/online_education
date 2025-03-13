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
from twilio.rest import Client
import random
from dotenv import load_dotenv
import os


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user=request.user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)
        return Response({"message": "Logged out successfully"})


class TelegramLoginView(APIView):
    def post(self, request):
        telegram_data = request.data  # Telegramdan kelgan ma'lumotlar

        # Telegramdan kelgan ma'lumotlarni tekshirish
        telegram_user_id = telegram_data.get('id')
        first_name = telegram_data.get('first_name')
        last_name = telegram_data.get('last_name')
        username = telegram_data.get('username')

        if not telegram_user_id:
            return Response({"error": "Telegram user ID talab qilinadi."}, status=status.HTTP_400_BAD_REQUEST)

        # Foydalanuvchini ro'yxatdan o'tkazish yoki yangilash
        user, created = User.objects.get_or_create(
            telegram_user_id=telegram_user_id,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'username': username or f'tg-{telegram_user_id}'  # Agar username bo'lmasa
            }
        )

        if not created:
            # Foydalanuvchi allaqachon mavjud bo'lsa, ma'lumotlarni yangilash
            user.first_name = first_name
            user.last_name = last_name
            user.username = username or user.username
            user.save()

        return Response({"message": "Muvaffaqiyatli ro'yxatdan o'tdingiz!", "user_id": user.id}, status=status.HTTP_200_OK)


class SendSMSView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({"error": "Telefon raqam kiritilmadi."}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(phone_number=phone_number)

        code = ''.join(random.choices('0123456789', k=6))
        user.sms_code = code
        user.save()

        account_sid = os.getenv('TWILIO_ACCOUNT_SID') 
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')    
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=f"Sizning tasdiqlash kodingiz: {code}",
            from_='+18774474810',  
            to=phone_number        
        )

        return Response({"message": "SMS kodi yuborildi."}, status=status.HTTP_200_OK)
    

class VerifySMSView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')
        if not phone_number or not code:
            return Response({"error": "Telefon raqam yoki kod kiritilmadi."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response({"error": "Foydalanuvchi topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        if user.sms_code != code:
            return Response({"error": "Noto'g'ri kod."}, status=status.HTTP_400_BAD_REQUEST)

        # Kodning amal qilish muddatini tekshirish (masalan, 5 daqiqa)
        # if timezone.now() - user.sms_code_created_at > timedelta(minutes=5):
        #     return Response({"error": "Kodning amal qilish muddati tugagan."}, status=status.HTTP_400_BAD_REQUEST)

        # Kodni tasdiqlash
        user.sms_code = None  # Kodni tozalash
        user.sms_code_created_at = None  # Vaqtni tozalash
        user.save()

        return Response({"message": "Kod tasdiqlandi."}, status=status.HTTP_200_OK)
