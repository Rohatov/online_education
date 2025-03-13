# Generated by Django 5.1.7 on 2025-03-12 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0005_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='total_duration',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='video',
            name='duration',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]
