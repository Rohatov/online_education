from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.models import User
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def create_jwt_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton("📱 Telefon raqamni ulashish", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True)
    
    await update.message.reply_text(
        "Salom! Iltimos, telefon raqamingizni ulashing:",
        reply_markup=reply_markup
    )

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.effective_message.contact

    if contact:
        phone_number = contact.phone_number
        user, created = User.objects.get_or_create(username=phone_number)

        if created:
            user.set_password(phone_number)  
            user.save()

        tokens = create_jwt_for_user(user)
        await update.message.reply_text(
            f"Access token: {tokens['access']}\nRefresh token: {tokens['refresh']}"
        )
    else:
        await update.message.reply_text("Telefon raqamingizni ulashishda xatolik yuz berdi.")

def run_bot():
    application = ApplicationBuilder().token("8111226311:AAGLEt9vhJf6sSozT94BxxvyF9AlstxkJM8").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    application.run_polling()
