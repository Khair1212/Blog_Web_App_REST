from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import PostViewSet, CommentViewSet, SharePostView

router1 = SimpleRouter()
router1.register('blogs', PostViewSet, basename='posts')

router2 = SimpleRouter()
router2.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router1.urls)),
    path('blogs/<int:pk>/', include(router2.urls)),
    path('blogs/<int:pk>/share_post/', SharePostView.as_view(), name="share_post")
]