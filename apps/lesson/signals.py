from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.lesson.models import Video

@receiver(post_save, sender=Video)
@receiver(post_delete, sender=Video)
def update_lesson_duration(sender, instance, **kwargs):
    """
    Video qo‘shilganda yoki o‘chirib tashlanganda umumiy davomiylikni yangilaydi.
    """
    instance.lesson.update_total_duration()
