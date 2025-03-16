from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.config.models import Basemodel
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
# from apps.telegram_bot.bot import receive_contact
import uuid
import random
# Create your models here.

# TEACHER, STUDENT = ('teacher', 'student')
VIA_PHONE = ('via_phone')

class User(Basemodel, AbstractUser):
    TEACHER = 'teacher'
    STUDENT = 'student'

    USER_ROLES = (
        (TEACHER, "Teacher"),
        (STUDENT, "Student")
    )
    telegram_user_id = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Telegram user ID',
        null=True,
        blank=True
    )
    phone_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Phone_number',
        # validators=[
        #     RegexValidator(
        #         regex=r'^\+998\d{8}$',
        #         message="Telefon raqami '+998912345678' kabi formatda bo'lishi kerak."
        #     )
        # ],
        null=True,
        blank=True
    )
    role = models.CharField(max_length=50, choices=USER_ROLES, default=STUDENT)
    sms_code = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        verbose_name='SMS code'
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name='Verified'
    )
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return f"User_id:{self.telegram_user_id}, Phone_number:{self.phone_number}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def check_username(self):
        if not self.username:
            temp_username = f'tg-{uuid.uuid4().hex[:8]}'
            while User.objects.filter(username=temp_username).exists():
                temp_username = f'{temp_username}{random.randint(0, 9)}'
            self.username = temp_username

    def clean(self):
        super().clean()
        if not self.is_superuser and not self.telegram_user_id and not self.phone_number:
            raise ValidationError("Telegram user ID yoki telefon raqami bo'lishi kerak.")
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.check_username()
        self.clean()
        super(User, self).save(*args, **kwargs)
