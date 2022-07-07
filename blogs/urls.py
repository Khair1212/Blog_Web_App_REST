from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import PostViewSet, CommentViewSet

router1 = SimpleRouter()
router1.register('blogs', PostViewSet, basename='posts')

router2 = SimpleRouter()
router2.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router1.urls)),
    path('blogs/<int:pk>/', include(router2.urls))
]