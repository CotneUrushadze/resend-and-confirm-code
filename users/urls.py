from django.urls import path, include
from users.views import UserViewSet, RegisterViewSet, ResetPasswordViewSet, ResetPasswordConfirmViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('register', RegisterViewSet, basename='register')
router.register('reset_password', ResetPasswordViewSet, basename='reset_password')


urlpatterns = [
    path('reset_password_confirm/<uidb64>/<token>', ResetPasswordConfirmViewSet.as_view({'post':'create'}), name='password-reset-confirm' ),
    path("", include(router.urls)),
]
    
     
