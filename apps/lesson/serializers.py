from rest_framework import serializers
from apps.accounts.models import User
from apps.lesson.models import Lesson, Comment, Category, Video, Section, Test, Rating

class LessonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
    

class VideoSerializers(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)
    view_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    class Meta:
        model = Video
        fields = '__all__'

    @staticmethod
    def get_comment_count(obj):
        count = obj.comments.count()
        return count
    
    @staticmethod
    def get_view_count(obj):
        count = obj.video_views.count()
        return count


class TestSerializers(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'


class SectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'
    

class SectionDetailSerializers(serializers.ModelSerializer):
    videos = VideoSerializers(many=True)
    tests = TestSerializers(many=True)
    class Meta:
        model = Section
        fields = '__all__'

class LessonDetailSerializers(serializers.ModelSerializer):
    sections = SectionDetailSerializers(many=True)
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'sections', 'comment_count', 'view_count', 'sections']


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CategorySerializers(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)
    class Meta:
        model = Category
        fields = '__all__'


class LikeToLessonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class LikeToRatingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class RatingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class ViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class NewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'