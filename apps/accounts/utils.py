from django.utils import timezone
import random
from twilio.rest import Client
from django.core.cache import cache


def generate_code():
    return str(random.randint(100000, 999999))

def send_sms(phone_number, code):
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
    cache.set(f"sms_time_{phone_number}", timezone.now().isoformat(), timeout=300)