from django.db.models.signals import post_save
from django.dispatch import receiver
from social_django.models import UserSocialAuth
from apps.accounts.models import User


@receiver(post_save,  sender=UserSocialAuth)
def save_profile_photo(sender, instance, created, update_fields,  **kwargs):
    
    if instance.extra_data:
        user = instance.user
        picture = instance.extra_data['photo_url']
        user.profile = picture
        user.save() 