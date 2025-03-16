from django.shortcuts import render
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
import random
from rest_framework import status
from datetime import timedelta
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.models import User
from twilio.rest import Client

def generate_code():
    return str(random.randint(100000, 999999))

def send_sms(phone_number, code, request):
    """Telefon raqamga SMS yuborish funksiyasi."""
    account_sid = 'AC61724543bdd36555dd3e5c768f99ab7c'
    auth_token = '9eb280209e2ec94f675a22dab7c07e33'
    client = Client(account_sid, auth_token)
    
    # message = client.messages.create(
    #     body=f"Sizning tasdiqlash kodingiz: {code}",
    #     from_='+18774474810',
    #     to=phone_number
    # )
    
    # print("SMS kodi yuborildi:", message.sid, code)
    print("SMS kodi yuborildi:", code)
    request.session[f"sms_time_{phone_number}"] = timezone.now().isoformat()
    a = request.session[f"sms_time_{phone_number}"] = timezone.now().isoformat()
    request.session.modified = True
    b = request.session[f"sms_time_{phone_number}"] = timezone.now().isoformat()
    print('######################################################')
    print(a)
    print('AAAAAA')
    print(b)
    return Response({"message": "SMS yuborildi",
                     "phone_number": phone_number}, status=status.HTTP_200_OK)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        role = request.data.get("role")
        phone_number = request.data.get("phone_number")

        if not all([first_name, last_name, role, phone_number]):
            return Response({"error": "Barcha maydonlar talab qilinadi."}, status=status.HTTP_400_BAD_REQUEST)

        if role not in [User.TEACHER, User.STUDENT]:
            return Response({"error": "Noto‘g‘ri rol tanlandi."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(phone_number=phone_number).exists():
            return Response({"error": "Bu telefon raqam bilan ro‘yxatdan o‘tgan foydalanuvchi mavjud."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            role=role,
            is_verified=False
        )
        
        sms_code = generate_code()
        user.sms_code = sms_code
        user.sms_code_created_at = timezone.now()
        user.save()
        
        send_sms(phone_number, sms_code)
        
        return Response({
            "message": "Ro‘yxatdan o‘tish muvaffaqiyatli yakunlandi. Iltimos, tasdiqlash kodini kiriting.",
            "phone_number": phone_number
        }, status=status.HTTP_201_CREATED)

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
        
        sms_time_str = request.session.get(f"sms_time_{phone_number}")
        print(sms_time_str)
        print(phone_number)

        sms_time = timezone.datetime.fromisoformat(sms_time_str)

        # 5 daqiqadan eski bo‘lsa xatolik qaytarish
        if timezone.now() - sms_time > timedelta(minutes=5):
            return Response({"error": "SMS kodi eskirgan"}, status=400)

        if user.sms_code != code:
            return Response({"error": "Noto‘g‘ri kod."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_verified = True
        user.sms_code = None
        user.sms_time = None
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "message": "Login muvaffaqiyatli amalga oshirildi."
        }, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({"error": "Telefon raqam talab qilinadi."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response({"error": "Foydalanuvchi topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        sms_code = generate_code()
        user.sms_code = sms_code
        user.sms_code_created_at = timezone.now()
        user.save()

        send_sms(phone_number, sms_code)


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
