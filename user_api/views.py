from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import *
from rest_framework import parsers
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.utils.datastructures import MultiValueDict

from django.core.files.storage import default_storage

from user_api.models import UserAccount
from user_api.serializers import *

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
# Create your views here.

import datetime
import pyrebase
import os
import json


config = {
    "apiKey": "AIzaSyCNvlmrJ4M-_wPcVyoBnXYpNZB9X7L98eI",
    "authDomain": "ristek-medsos.firebaseapp.com",
    "projectId": "ristek-medsos",
    "storageBucket": "ristek-medsos.appspot.com",
    "messagingSenderId": "858790958092",
    "appId": "1:858790958092:web:ff905012004b4bc2a34a29",
    "measurementId": "G-6RD9FMRL86",
    "databaseURL":""
}

firebase = pyrebase.initialize_app(config)
storage_firebase = firebase.storage()



class LogoutView(APIView):
    def get(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'Logout'
        }
        return response

class RegisterView(APIView):
    def post(self, request):
        req_body = parsers.JSONParser().parse(request)
        serializer = UserSerializer(data=req_body)
        if serializer.is_valid():
            user = UserAccount.objects.create(username=req_body['username'], password=req_body['password'], name=req_body['name'], bio = req_body['bio'])
            user.set_password(req_body['password'])
            user.save()
            return Response(serializer.data)
        else:
            return Response({'message':serializer.errors})

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request):
        try:
            user = UserAccount.objects.get(pk=request.user.pk)
            user.name = request.POST.get('payload[name]')
            user.bio = request.POST.get('payload[bio]')
            
            file = request.FILES.get('payload[profile_picture]')
            file_save = default_storage.save(file.name, file)
            storage_firebase.child("static/" + file.name).put("static/" + file.name)
            delete = default_storage.delete(file.name)

            user.profile_picture = file.name
            user.save()
            serializer = UserSerializer(user)
            return Response({'message':"Successfully changed"}, status=200)
        except:
            return Response({'message':"An error has occured"})


class CloseFriendsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        req_body = parsers.JSONParser().parse(request)
        try:
            user = UserAccount.objects.get(pk=request.user.pk)

            user.close_friends.set(req_body['close_friends'])
            user.close_friends.add(request.user.pk)
            user.save()
            serializer = UserSerializer(user)
        except:
            return Response({'message':"An error has occured"})

        return Response(serializer.data)

class GetToken(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'jwt':'tes'})
    
class GetAllUsers(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = UserAccount.objects.all()
            serializer = AllUsernameSerializer(user, many=True, context=request)
            return Response(serializer.data)
        except:
            return Response({'message':"An error has occured"})
