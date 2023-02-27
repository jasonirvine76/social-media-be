from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from user_api.viewsets import *
from user_api.views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register('login', UserViewSet)

app_name = 'auth'

urlpatterns = [
    path('', include(router.urls)),
    # path(r'^auth/', include('djoser.urls')),
    # path(r'^auth/', include('djoser.urls.jwt')),
    path('logout/', LogoutView.as_view()),
    path('change-profile/', UpdateProfileView.as_view()),
    path('register/', RegisterView.as_view()),
    path('close-friends/', CloseFriendsView.as_view()),
    path('token/', GetToken.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('all-users/', GetAllUsers.as_view()),
]