from django.db import models
from apps.config.models import Basemodel
from apps.accounts.models import User
from django.core.validators import FileExtensionValidator
from mptt.models import MPTTModel, TreeForeignKey


class Category(Basemodel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Lesson(Basemodel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons')
    image = models.ImageField(upload_to='course images/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_lessons')
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_profession = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

class Section(Basemodel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return self.title


class Video(Basemodel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='videos')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='section_videos')
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to='course/',
    validators=[FileExtensionValidator(
        allowed_extensions=['.mp4', '.avi', '.mov', '.mkv'],
        message='Faqat quyidagi formatlardagi fayllar qabul qilinadi: MP4, AVI, MOV, MKV.'
        )],
    )

    def __str__(self):
        return self.title


class Comment(Basemodel, MPTTModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE,)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    count = models.PositiveIntegerField(default=0)


    class MPTTMeta:
        order_insertion_by = ['id']

    def __str__(self):
        parent_info = f"Reply to {self.parent.author}" if self.parent and self.parent.author else "Deleted message"
        return f"{self.author} - {parent_info} - {self.lesson}"

    def get_parent_text(self):
        if self.parent:
            return self.parent.text if self.parent.text else "Deleted message"
        return "Deleted message"
    

class View(Basemodel):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_views')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_views')
    

class LikeToVideo(Basemodel):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_likes')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_likes')
    dislike = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author} - {self.video}"


class LikeToComment(Basemodel):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_comment_likes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_likes')
    dislike = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author} - {self.comment}"