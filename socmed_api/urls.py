from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from socmed_api.viewsets import *
from socmed_api.views import *

router = routers.DefaultRouter()
router.register('home', FeedViewSet)

app_name = 'feed'

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', GetFeeds.as_view())
]