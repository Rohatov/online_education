from telegram.ext import ApplicationBuilder

def run_bot():
    application = ApplicationBuilder().token("8111226311:AAGLEt9vhJf6sSozT94BxxvyF9AlstxkJM8").build()
    application.run_polling()

if __name__ == "__main__":
    run_bot()
