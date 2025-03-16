from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.lesson.models import Lesson, Video, Comment, Category, Test, Section, Rating, LikeToLesson, View, LikeToRating, News
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from apps.lesson.serializers import (LessonSerializers, CommentSerializers, VideoSerializers,
                                    CategorySerializers, LessonDetailSerializers, TestSerializers,
                                    NewsSerializers, SectionSerializers, SectionDetailSerializers, 
                                    RatingSerializers, LikeToLessonSerializers,LikeToRatingSerializers)
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
    serializer_class = CategorySerializers

    def patch(self, request, pk):
        item = Category.objects.get(id=pk)
        if item.author == request.user:
            data = request.data
            serializer = self.serializer_class(instance=item, data=data, context={'request': request}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data = serializer.data)
        else:
            data = {
                'status': False,
                'message': 'Siz kategoriyaning muallifi emassiz'
            }
            raise ValidationError(data)

    def put(self, request, pk):
        item = Category.objects.get(id=pk)
        if item.author == request.user:
            data = request.data
            serializer = self.serializer_class(instance=item, data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data = serializer.data)
        else:
            data = {
                'status': False,
                'message': 'Siz kategoriyaning muallifi emassiz'
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
                'message': 'Siz kategoriyaning muallifi emassiz'
            }
            raise ValidationError(data)


class LessonAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializers
    
    def get(self, request):
        lessons = Lesson.objects.all()
        serializer = self.serializer_class(lessons, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        data['author'] = request.user.id
        serializer = self.serializer_class(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LessonDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonDetailSerializers

    def get_object(self, pk):
        obj = get_object_or_404(Lesson, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = self.serializer_class(item, context={'request': request})
        return Response(serializer.data)
    
    def patch(self, request, pk):
        item = self.get_object(pk)
        if item.author == request.user:
            data = request.data
            serializer = self.serializer_class(instance=item, data=data, context={'request': request}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data = serializer.data)
        else:
            data = {
                'status': False,
                'message': 'Siz ushbu darsning muallifi emassiz'
            }
            raise ValidationError(data)

    def put(self, request, pk):
        item = self.get_object(pk)
        if item.author == request.user:
            data = request.data
            serializer = self.serializer_class(instance=item, data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data = serializer.data)
        else:
            data = {
                'status': False,
                'message': 'Siz ushbu darsning muallifi emassiz'
            }
            raise ValidationError(data)
        
    def delete(self, request, pk):
        item = self.get_object(pk)
        if item.author == request.user:
            item.delete()
            return Response({"msg": "successfully deleted"})
        else:
            data = {
                'status': False,
                'message': 'Siz ushbu darsning muallifi emassiz'
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
    serializer_class = VideoSerializers

    def get_object(self, pk):
        obj = get_object_or_404(Video, id=pk)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get(self, request, pk):
        item = self.get_object(pk)
        user = request.user if request.user.is_authenticated else None
        view_exists = View.objects.filter(author=user, video=item).exists()
        if not view_exists:
            View.objects.create(author=user, video=item)
            item.video_views +=1
            item.save()
        serializer = self.serializer_class(item)
        return Response(serializer.data)

    def patch(self, request, pk):
        item = self.get_object(pk)
        if item.author == request.user:
            data = request.data
            serializer = self.serializer_class(instance=item, data=data, context={'request': request}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"msg": "video muvaffaqiyatli o'zgartirildi"}, status=status.HTTP_200_OK)
        else:
            data = {
                'status': False,
                'msg': 'Siz videoning muallifi emassiz'
            }
            raise ValidationError(data)

    def put(self, request, pk):
        item = self.get_object(pk)
        if item.author == request.user:
            data = request.data
            serializer = self.serializer_class(instance=item, data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data = serializer.data)
        else:
            data = {
                'status': False,
                'message': 'Siz videoning muallifi emassiz'
            }
            raise ValidationError(data)
        
    def delete(self, request, pk):
        item = self.get_object(pk)
        if item.author == request.user:
            item.delete()
            return Response({"msg": "video muvaffaqiyatli o'chirildi"})
        else:
            data = {
                'status': False,
                'message': 'Siz videoning muallifi emassiz'
            }
            raise ValidationError(data)
        

class TestApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TestSerializers

    def get(self, request):
        tests = Test.objects.filter(is_active=True)
        serializer = self.serializer_class(tests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TestSerializers

    def get_object(self, pk):
        obj = get_object_or_404(Test, id=pk)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def patch(self, request, pk):
        item = self.get_object(pk)
        if item.author == request.user:
            data = request.data
            serializer = self.serializer_class(instance=item, data=data, context={'request': request}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data = serializer.data)
        else:
            data = {
                "status": False,
                "msg": "Siz ushbu testning muallifi emassiz"            
            }
            return Response(data)
    
    def put(self, request, pk):
        item = self.get_object(pk)
        if item.author == request.user:
            data = request.data
            serializer = self.serializer_class(instance=item, data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data = serializer.data)
        else:
            data = {
                "status": False,
                "msg": "Siz ushbu testning muallifi emassiz"            
            }
            return Response(data)
        
    def delete(self, request, pk):
        item = self.get_object(pk)
        if item.author == request.user:
            item.delete()
            return Response({"msg": "test muvaffaqiyatli o'chirildi"})
        else:
            data = {
                "status": False,
                "msg": "Siz ushbu testning muallifi emassiz"            
            }
            return Response(data)
        

class CommentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializers
    
    def get(self, request):
        comments = Comment.objects.all()
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializers

    def get_object(self, pk):
        obj = get_object_or_404(Lesson, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = self.serializer_class(item)
        return Response(serializer.data)
    
    def patch(self, request, pk):
        item = self.get_object(pk)
        if item.author == request.user:
            data = request.data
            serializer = self.serializer_class(instance=item, data=data, context={'request': request}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data = serializer.data)
        else:
            data = {
                'status': False,
                'message': 'Siz ushbu sharh ning muallifi emassiz'
            }
            raise ValidationError(data)

    def put(self, request, pk):
        item = self.get_object(pk)
        if item.author == request.user:
            data = request.data
            serializer = self.serializer_class(instance=item, data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data = serializer.data)
        else:
            data = {
                'status': False,
                'message': 'Siz ushbu sharh ning muallifi emassiz'
            }
            raise ValidationError(data)
        
    def delete(self, request, pk):
        item = self.get_object(pk)
        if item.author == request.user:
            item.delete()
            return Response({"msg": "sharh muvaffaqiyatli o'chirildi"})
        else:
            data = {
                'status': False,
                'message': 'Siz ushbu sharh ning muallifi emassiz'
            }
            raise ValidationError(data)
    

class SearchListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializers

    def get_queryset(self):
        query = self.request.GET.get("query", "").strip()
        if not query:
            return Lesson.objects.none()
        return Lesson.objects.filter(title__icontains=query)
    

class OrderByTimeView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializers

    def get_queryset(self):
        return Lesson.objects.order_by('-created_at')
    

class NewsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serialzier_class = NewsSerializers
    def get(self, request):
        news = News.objects.all()
        serializer = self.serialzier_class(news, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.serialzier_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NewsSerializers

    def get_object(self, pk):
        obj = get_object_or_404(News, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = self.serializer_class(item, context={'request': request})
        return Response(serializer.data)
    
    def patch(self, request, pk):
        item = self.get_object(pk)
        if item.author == request.user:
            data = request.data
            serializer = self.serializer_class(instance=item, data=data, context={'request': request}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data = serializer.data)
        else:
            data = {
                'status': False,
                'message': 'Siz ushbu News ning muallifi emassiz'
            }
            raise ValidationError(data)
        
    def put(self, request, pk):
        item = self.get_object(pk)
        if item.author == request.user:
            data = request.data
            serializer = self.serializer_class(instance=item, data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data = serializer.data)
        else:
            data = {
                'status': False,
                'message': 'Siz ushbu News ning muallifi emassiz'
            }
            raise ValidationError(data)
    
    def delete(self, request, pk):
        item = self.get_object(pk)
        if item.author == request.user:
            item.delete()
            return Response({"msg": "News muvaffaqiyatli o'chirildi"})
        else:
            data = {
                'status': False,
                'message': 'Siz ushbu News ning muallifi emassiz'
            }
            raise ValidationError(data)


class SectionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SectionSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SectionDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SectionDetailSerializers

    def get_object(self, pk):
        obj = get_object_or_404(Section, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = self.serializer_class(item, context={'request': request})
        return Response(serializer.data)
    
    def patch(self, request, pk):
        item = self.get_object(pk)
        if item.author == request.user:
            data = request.data
            serializer = self.serializer_class(instance=item, data=data, context={'request': request}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data = serializer.data)
        else:
            data = {
                'status': False,
                'message': 'Siz ushbu bo`limning muallifi emassiz'
            }
            raise ValidationError(data)
    
    def delete(self, request, pk):
        item = self.get_object(pk)
        if item.author == request.user:
            item.delete()
            return Response({"msg": "Bo`lim muvaffaqiyatli o`chirildi"})
        else:
            data = {
                'status': False,
                'message': 'Siz ushbu bo`limning muallifi emassiz'
            }
            raise ValidationError(data)
        

class RatingAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RatingSerializers

    def get(self, request):
        ratings = Rating.objects.all()
        serializer = self.serializer_class(ratings, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RatingDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RatingSerializers

    def get_object(self, pk):
        obj = get_object_or_404(Rating, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def delete(self, request, pk):
        item = self.get_object(pk)
        if item.author == request.user:
            item.delete()
            return Response({"msg": "Sharh muvaffaqiyatli o`chirildi"})
        else:
            data = {
                'status': False,
                'message': 'Siz ushbu Sharh muallifi emassiz'
            }
            raise ValidationError(data)
        

class LikeToLessonAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeToLessonSerializers

    def post(self, request):
        user = request.user
        pk = request.data.get('lesson')
        like, created = LikeToLesson.objects.get_or_create(author=user, lesson_id=pk)
        if not created:
            like.delete()
        if created:
            like.like = True
            like.save()
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LikeToRatingAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeToRatingSerializers

    def post(self, request):
        user = request.user
        pk = request.data.get('rating')
        like, created = LikeToRating.objects.get_or_create(author=user, rating_id=pk)
        dislike = request.data.get('dislike', False)
        if not created:
            if like.dislike == dislike:
                like.delete()
                return Response({"msg": "like o'chirildi" if not like.dislike else "dislike o'chirildi"}, status=status.HTTP_204_NO_CONTENT)
            else:
                like.dislike = dislike
                like.save()
                return Response({"msg": "like dislike ga o'zgartirildi" if like.dislike else "dislike like ga o'zgartirildi"}, status=status.HTTP_200_OK)
        like.dislike = dislike
        like.save()
        return Response({"msg": "like qilindi" if not like.dislike else "dislike qilindi"}, status=status.HTTP_201_CREATED)

