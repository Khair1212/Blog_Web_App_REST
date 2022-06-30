from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import SimpleRouter
from .views import UserView, PasswordResetView, PasswordConfirmView, AccountActiveOrResetView

router = SimpleRouter()
router.register(r'users', UserView, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/account_active/<umail>/', AccountActiveOrResetView.as_view(), name = 'account_active'),
    path('api/password-reset/', PasswordResetView.as_view(), name='password_reset' ),
    path('api/confirm-password/<uid>/<token>/', PasswordConfirmView.as_view(), name= 'confirm_password')
]
