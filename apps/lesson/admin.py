from django.contrib import admin
from apps.lesson.models import Lesson, Video, Comment, Category
# Register your models here.

class VideoInline(admin.TabularInline):
    model = Video
    extra = 3


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_at', 'update_at')
    list_filter = ('create_at', 'update_at')
    search_fields = ('name',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'create_at', 'update_at')
    list_filter = ('author', 'title', 'create_at', 'update_at')
    search_fields = ('title', 'create_at', 'update_at')
    inlines = [VideoInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'video', 'create_at', 'parent')
    list_filter = ('author', 'video', 'create_at')
    search_fields = ('author', 'video', 'create_at')
