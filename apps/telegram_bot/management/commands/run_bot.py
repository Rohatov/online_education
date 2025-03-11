from django.core.management.base import BaseCommand
from apps.telegram_bot.run_bot import run_bot

class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **kwargs):
        run_bot()
