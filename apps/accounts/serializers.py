from rest_framework import serializers
from apps.accounts.utils import generate_code, send_sms
from django.core.cache import cache
from django.utils import timezone
from apps.accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'role', 'phone_number', 'password', 'confirm_password')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Parollar bir-biriga mos kelmadi")
        
        if data['role'] not in [User.TEACHER, User.STUDENT]:
            raise serializers.ValidationError({"role": "Noto‘g‘ri rol tanlandi."})

        if User.objects.filter(phone_number=data['phone_number']).exists():
            raise serializers.ValidationError({"phone_number": "Bu telefon raqam bilan foydalanuvchi mavjud."})
        
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.is_verified = False

        sms_code = generate_code()
        user.sms_code = sms_code
        user.save()

        send_sms(user.phone_number, sms_code)
        self.context['sms_code'] = sms_code

        return user
    

class VerifySmsSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13)
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        code = attrs.get('code')

        if not phone_number or not code:
            raise serializers.ValidationError({"error": "Telefon raqam yoki kod kiritilmadi"})
        
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "Foydalanuvchi topilmadi"})
        
        sms_time = cache.get(f"sms_time_{phone_number}")

        if not sms_time:
            raise serializers.ValidationError({"error": "Sms kod topilmadi yoki eskirgan"})
        
        if user.sms_code != code:
            raise serializers.ValidationError({"error": "Noto'g'ri kod"})
        
        attrs['user'] = user
        return attrs
    

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "Foydalanuvchi topilmadi"})
        
        if not user.check_password(password):
            raise serializers.ValidationError({"error": "Notogri parol"})
        
        self.context['user'] = user
        return data