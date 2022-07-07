from django.shortcuts import render
from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, PostCreateSerializer, PostUpdateSerializer, CommentCreateSerializer, \
    CommentSerializer, CommentUpdateSerializer
from rest_framework import permissions
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination


# Create your views here.

# Pagination Class
class Pagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'
    # page_size_query_param = 'records
    max_page_size = 10
    # last_page_strings = 'end'


# Post viewSet Class

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    lookup_field = 'id'
    pagination_class = Pagination

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'title', 'created_by']
    search_fields = ['title', 'description', 'created_by__name', 'status']
    # ordering_fields = ['id', 'title', 'description', 'created_by', 'status']

    default_serializer_class = PostSerializer
    serializer_classes = {
        'list': PostSerializer,
        'create': PostCreateSerializer,
        'update': PostUpdateSerializer,
        'partial_update': PostUpdateSerializer,
    }

    # Get Serializer for specific action
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [permissions.IsAuthenticated, ]
        elif self.action == 'list':
            self.permission_classes = [permissions.AllowAny, ]
        else:
            self.permission_classes = [IsAuthorOrReadOnly, ]
        return [permission() for permission in self.permission_classes]

    # Create Post
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = PostCreateSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                self.perform_create(serializer)
            return Response({'message': f'Post has been published!'},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            error = f'Server Error: {e}'
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Post List
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            # ordering = ['-created']

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            error = f'Server Error: {e}'
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            error = f'Server Error: {e}'
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, **kwargs):
        try:
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
        except Exception as e:
            error = f'Server Error: {e}'
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Delete Post
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": f"Post titled '{instance.title}' has been deleted!"},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error = f'Server Error: {e}'
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_destroy(self, instance):
        instance.delete()

    # @action(methods=['get'], detail=True)
    # def comments(self, request, pk=None):
    #     try:
    #         post = Post.objects.get(id=pk)
    #     except Post.DoesNotExist:
    #         return Response({"error": "Post not found. "}, status=status.HTTP_400_BAD_REQUEST)
    #     comments = post.comments.all()
    #     return Response(CommentSerializer(comments, many=True))


# Comment Viewset
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    lookup_field = 'id'

    default_serializer_class = CommentSerializer
    serializer_classes = {
        'list': CommentSerializer,
        'create': CommentCreateSerializer,
        # 'update': CommentUpdateSerializer,
        # 'partial_update': CommentUpdateSerializer
    }

    # Get Serializer for specific action
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [permissions.IsAuthenticated, ]
        elif self.action == 'list':
            self.permission_classes = [permissions.AllowAny, ]
        else:
            self.permission_classes = [IsAuthorOrReadOnly, ]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, post, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):

        try:
            data = request.data
            serializer = CommentCreateSerializer(data=data,)
            post = Post.objects.get(id=kwargs.get('pk'))
            print(post)
            if serializer.is_valid(raise_exception=True):
                # self.perform_create(serializer)
                serializer.save(comment_by=request.user, post=post)

                return Response(serializer.data)
            return Response({'message': f'Comment Added to post'},
                                status=status.HTTP_201_CREATED)
        except Exception as e:
            error = f'Server Error: {e}'
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_update(self, serializer):
        serializer.save(comment_by=self.request.user)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
            post = Post.objects.get(id=kwargs.get('pk'))
            if serializer.is_valid():
                serializer.save(comment_by=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            error = f'Server Error: {e}'
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message': 'The comment has been deleted!'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error = f'Server Error: {e}'
            return Response({'message': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        def perform_destroy(self, instance):
            instance.delete()