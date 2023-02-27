from rest_framework import viewsets
from rest_framework import parsers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import action

from django.shortcuts import render 
from django.http import HttpResponse, HttpResponseNotFound

from user_api.models import UserAccount
from user_api.serializers import UserSerializer

import jwt, datetime


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def list(self ,request):
        try:
            data_user = UserAccount.objects.get(username=request.user.pk)
            serializer = self.serializer_class(data_user)
            return Response(serializer.data)
        except:
            return Response({'message':'User not found'})

    def create(self, request):
        username = request.data['username']
        password = request.data['password']


        user = UserAccount.objects.get(username=username)

        if user is None:
            raise AuthenticationFailed("User not found!")
        
        if not user.check_password(password):
            raise AuthenticationFailed("User not found or incorrect password")

        serializer = self.serializer_class(user)

        payload = {
            'id': user.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm = 'HS256')
        
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt':token
        }
        return response

    




    


    