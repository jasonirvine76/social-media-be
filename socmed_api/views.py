from rest_framework import viewsets
from rest_framework import parsers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import AuthenticationFailed

from django.shortcuts import render 
from django.http import HttpResponse, HttpResponseNotFound

from socmed_api.models import Feed
from socmed_api.serializers import FeedSerializer, GetFeedSerializer
from user_api.models import UserAccount

# Create your views here.
class GetFeeds(APIView):
    def get(self, request):
        try:
            feeds = Feed.objects.all()[0]
            serializer = GetFeedSerializer(feeds, context=request)
            return Response(serializer.data)
        except:
            return Response([])