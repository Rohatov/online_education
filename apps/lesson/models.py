from django.db import models
from apps.config.models import Basemodel
from apps.accounts.models import User
from django.core.validators import FileExtensionValidator
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
import moviepy as mp

class Category(Basemodel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Lesson(Basemodel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons')
    image = models.ImageField(upload_to='media/course images/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_lessons')
    title = models.CharField(max_length=255)
    description = models.TextField()
    total_duration = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return self.title
    
    def update_total_duration(self):
        """
        Barcha bog‘langan videolar uzunligini hisoblab chiqadi.
        """
        self.total_duration = sum(video.duration for video in self.videos.all())
        self.save()

    def average_rating(self):
        ratings = self.lesson_ratings.all()
        if ratings.exists():
            return sum(r.rating for r in ratings) / ratings.count()
        return 0
    

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
    video = models.FileField(upload_to='media/course/',
    validators=[FileExtensionValidator(
        allowed_extensions=['.mp4', '.avi', '.mov', '.mkv'],
        message='Faqat quyidagi formatlardagi fayllar qabul qilinadi: MP4, AVI, MOV, MKV.'
        )],
    )
    duration = models.PositiveIntegerField(default=0, editable=False) 

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """
        Video fayli yuklangandan so‘ng, avtomatik ravishda davomiyligini aniqlaydi.
        """
        if self.video:
            video_path = self.video.path
            clip = mp.VideoFileClip(video_path)
            self.duration = round(clip.duration / 60)  
            clip.close()

        super().save(*args, **kwargs)


class Test(Basemodel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tests')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_tests')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='section_test')
    question = RichTextField()
    answer_choice = models.JSONField()
    corrrect_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.question} - {self.corrrect_answer}"



class Comment(Basemodel, MPTTModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE,)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
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
    

class LikeToLesson(Basemodel):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_likes')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_likes')
    like = models.BooleanField()

    def __str__(self):
        return f"{self.author} - {self.lesson}"
    

class Rating(Basemodel):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_ratings')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_ratings')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ['author', 'lesson']
    
    def __str__(self):
        return f"{self.author} - {self.lesson} - {self.rating}"


class LikeToRating(Basemodel):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_comment_likes')
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, related_name='rating_likes')
    dislike = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author} - {self.rating}"
    

class News(Basemodel):
    title = models.CharField(max_length=255)
    body = RichTextField()
    image = models.ImageField(upload_to='media/news images/', null=True, blank=True)

    def __str__(self):
        return self.title


