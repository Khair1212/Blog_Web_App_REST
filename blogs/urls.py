from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import PostViewSet, CommentViewSet

router = SimpleRouter()
router.register('blogs', PostViewSet, basename='posts')
router.register('blogs/<int:pk>/comments/', CommentViewSet, basename = 'comments')

urlpatterns = [
    path('', include(router.urls))
]