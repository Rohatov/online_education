# Generated by Django 5.1.5 on 2025-01-25 16:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('lesson', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_views', to='accounts.user')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_views', to='lesson.lesson')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
