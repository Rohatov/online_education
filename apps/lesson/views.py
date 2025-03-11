from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.lesson.models import Lesson, Video, Comment, Category
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from apps.lesson.serializers import LessonSerializers, CommentSerializers, VideoSerializers, CategorySerializers
# Create your views here.


class CategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializers(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CategorySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CategoryDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        item = Category.objects.get(id=pk)
        if item.author == request.user:
            data = request.data
            serializer = CategorySerializers(instance=item, data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data = serializer.data)
        else:
            data = {
                'status': False,
                'message': 'You not author is category or not authenticated'
            }
            raise ValidationError(data)
        
    def delete(self, request, pk):
        item = Category.objects.get(id=pk)
        if item.author == request.user:
            item.delete()
            return Response({"msg": "successfully deleted"})
        else:
            data = {
                'status': False,
                'message': 'You not author is category or not authenticated'
            }
            raise ValidationError(data)


class LessonAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        lessons = Lesson.objects.all()
        serializer = LessonSerializers(lessons, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = LessonSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LessonDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            item = Lesson.objects.get(id=pk)
        except Lesson.DoesNotExist:
            Http404("Lesson does not exists")

    def put(self, request, pk):
        item = Lesson.objects.get(id=pk)
        if item.author == request.user:
            data = request.data
            serializer = LessonSerializers(instance=item, data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data = serializer.data)
        else:
            data = {
                'status': False,
                'message': 'You not author is lesson or not authenticated'
            }
            raise ValidationError(data)
        
    def delete(self, request, pk):
        item = Lesson.objects.get(id=pk)
        if item.author == request.user:
            item.delete()
            return Response({"msg": "successfully deleted"})
        else:
            data = {
                'status': False,
                'message': 'You not author is lesson or not authenticated'
            }
            raise ValidationError(data)
        

class VideoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoSerializers(videos, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = VideoSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class VideoDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            item = Video.objects.get(id=pk)
            serializer = VideoSerializers(item)
            return Response(serializer.data)
        except Video.DoesNotExist:
            raise Http404("Video does not exist")

    def put(self, request, pk):
        item = Video.objects.get(id=pk)
        if item.author == request.user:
            data = request.data
            serializer = VideoSerializers(instance=item, data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data = serializer.data)
        else:
            data = {
                'status': False,
                'message': 'You not author is video or not authenticated'
            }
            raise ValidationError(data)
        
    def delete(self, request, pk):
        item = Video.objects.get(id=pk)
        if item.author == request.user:
            item.delete()
            return Response({"msg": "successfully deleted"})
        else:
            data = {
                'status': False,
                'message': 'You not author is video or not authenticated'
            }
            raise ValidationError(data)
        

class CommentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializers(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CommentSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            item = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            raise Http404("Comment does not exist")
        serializer = CommentSerializers(instance=item)
        data = {        
            "data": serializer.data,
        }
        return Response(data=data)

    def put(self, request, pk):
        item = Comment.objects.get(id=pk)
        if item.author == request.user:
            data = request.data
            serializer = CommentSerializers(instance=item, data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data = serializer.data)
        else:
            data = {
                'status': False,
                'message': 'You not author is comment or not authenticated'
            }
            raise ValidationError(data)
        
    def delete(self, request, pk):
        item = Comment.objects.get(id=pk)
        if item.author == request.user:
            item.delete()
            return Response({"msg": "successfully deleted"})
        else:
            data = {
                'status': False,
                'message': 'You not author is comment or not authenticated'
            }
            raise ValidationError(data)

