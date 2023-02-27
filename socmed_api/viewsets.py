from rest_framework import viewsets
from rest_framework import parsers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import AuthenticationFailed

from django.shortcuts import render 
from django.http import HttpResponse, HttpResponseNotFound

from socmed_api.models import Feed
from socmed_api.serializers import FeedSerializer, GetFeedSerializer
from user_api.models import UserAccount

class FeedViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    permission_classes = [IsAuthenticated]


    def list(self ,request):
        
        feeds = Feed.objects.all()[0]
        serializer = GetFeedSerializer(feeds, context=request)
        return Response({'message':'Nothing showed here'})
        

    def create(self, request):
        
        req_body = parsers.JSONParser().parse(request)
        req_body['user'] = request.user.username
        serializer = self.serializer_class(data = req_body)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'Message':'Your input was wrong'})
        
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            feed = Feed.objects.get(id=pk, user=request.user.username)
            if feed is None:
                return Response({'message':'Not found'})
            feed.delete()
            return HttpResponse(b"DELETED", status=201)
        except:
            return Response({'message':'An error has occured'})

    def partial_update(self, request,  pk=None, *args, **kwargs):

        req_body = parsers.JSONParser().parse(request)
        try:
            feed = Feed.objects.get(id=pk, user=request.user.pk)
            feed.feed_msg = req_body['feed_msg']
            feed.visibility_to_close_friends = req_body['visibility_to_close_friends']
            feed.save()
            serializer = self.serializer_class(feed)
        except:
            return Response({'message':"An error has occured"})

        return Response(serializer.data)

    