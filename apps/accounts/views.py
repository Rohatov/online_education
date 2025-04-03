from django.shortcuts import render
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import status
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.models import User
from apps.accounts.serializers import UserRegisterSerializer, VerifySmsSerializer, LoginSerializer
from django.core.cache import cache
from apps.accounts.utils import generate_code, send_sms


class RegisterView(APIView):
    """register api da first_name"""
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "Ro‘yxatdan o‘tish muvaffaqiyatli yakunlandi. Iltimos, tasdiqlash kodini kiriting.",
            "phone_number": user.phone_number,
            "sms_code": serializer.context.get('sms_code')
        }, status=status.HTTP_201_CREATED)


class VerifySMSView(APIView):
    """verify-sms api da phone_number va code kiritiladi"""
    permission_classes = [AllowAny]
    serializer_class = VerifySmsSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
        
            user.is_verified = True
            user.sms_code = None
            user.sms_time = None
            user.save()
            
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "Sms muvaffaqiyatli tasdiqlandi"
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Foydalanuvchi Login qilishda birnchi phone_number kiritiladi keyin foydalanuvchi raqamiga sms habar yuboriladi
    undan keyin verify-sms api orqali sms tasdiqlanadi shundan song foydalanuvchiga refresh va acsess token beriladi"""
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = serializer.context['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "message": "Login muvaffaqiyatli amalga oshirildi."
                }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
