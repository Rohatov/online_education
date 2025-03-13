from django.apps import AppConfig


class LessonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.lesson'

    def ready(self):
        import apps.lesson.signals
