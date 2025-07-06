# Online Education

Online Education — bu zamonaviy mobil va veb platforma bo‘lib, foydalanuvchilarga istalgan joyda va vaqtda sifatli ta’lim olish imkonini beradi. Ilova orqali foydalanuvchilar fanlar bo‘yicha video darslarni ko‘rishlari, interaktiv testlar yordamida bilimlarini mustahkamlashlari va o‘qituvchilar bilan bevosita muloqot qilishlari mumkin.

## Xususiyatlari

- **Video darslar**: Turli sohalar bo‘yicha sifatli video darslar.
- **Interaktiv testlar**: Darslarni mustahkamlovchi test va viktorinalar.
- **Foydalanuvchi boshqaruvi**: O‘qituvchi va o‘quvchi rollari, telefon raqami orqali ro‘yxatdan o‘tish va SMS orqali tasdiqlash.
- **Izoh va fikrlar**: Har bir darsga fikr va izohlar yozish.
- **Telegram bilan integratsiya**: Telegram orqali tez ro‘yxatdan o‘tish va aloqa o‘rnatish.

## Texnologiyalar

- **Backend**: Django 5, Django REST Framework
- **JWT**: Avtorizatsiya va tokenlar uchun
- **SQLite** (standart), PostgreSQL (ishlab chiqarish uchun)
- **CKEditor**: Matn tahriri uchun
- **Telegram Bot**: Foydalanuvchi autentifikatsiyasi va bildirishnomalar uchun
- **Jazzmin**: Django admin interfeysini zamonaviylashtirish uchun

## O‘rnatish

1. Loyihani klonlang:
    ```bash
    git clone https://github.com/Rohatov/online_education.git
    cd online_education
    ```

2. Virtual muhit yarating va kerakli kutubxonalarni o‘rnating:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows uchun: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. Migratsiyalarni bajaring:
    ```bash
    python manage.py migrate
    ```

4. Superuser yarating:
    ```bash
    python manage.py createsuperuser
    ```

5. Serverni ishga tushiring:
    ```bash
    python manage.py runserver
    ```

## API hujjati

- Swagger: [`/swagger/`](http://localhost:8000/swagger/)
- Redoc: [`/redoc/`](http://localhost:8000/redoc/)

## Litsenziya

MIT

---
