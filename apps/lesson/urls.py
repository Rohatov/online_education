from django.urls import path
from apps.lesson.views import (CategoryAPIView, CategoryDetailAPIView, LessonAPIView, LessonDetailAPIView,
                               VideoAPIView, VideoDetailAPIView, TestApiView, TestDetailApiView, CommentAPIView,
                               CommentDetailAPIView)

app_name = 'lesson'

urlpatterns = [
    path('category/', CategoryAPIView.as_view(), name='category'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('lesson/', LessonAPIView.as_view(), name='lesson'),
    path('lesson/<int:pk>/', LessonDetailAPIView.as_view(), name='lesson_detail'),
    path('video/', VideoAPIView.as_view(), name='video'),
    path('video/<int:pk>/', VideoDetailAPIView.as_view(), name='video_detail'),
    path('test/', TestApiView.as_view(), name='test'),
    path('test/<int:pk>/', TestDetailApiView.as_view(), name='test_detail'),
    path('comment/', CommentAPIView.as_view(), name='comment'),
    path('comment/<int:pk>/', CommentDetailAPIView.as_view(), name='comment_detail'),
]