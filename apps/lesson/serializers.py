from rest_framework import serializers
from apps.lesson.models import Lesson, Comment, Category, Video

class LessonSerializers(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    view_count = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = '__all__'

    @staticmethod
    def get_comment_count(obj):
        count = obj.comments.count()
        return count


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    
class VideoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'