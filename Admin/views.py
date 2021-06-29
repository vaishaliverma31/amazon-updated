import datetime

from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .serializers import *
from user.models import User
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView, RetrieveUpdateAPIView, \
    UpdateAPIView
from rest_framework import generics, status
import json


# Create your views here.
class registeradminapi(APIView):
    def post(self, request):
        serializer = admin_serializer(data=self.request.data)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            user_query = User.objects.create_user(username=self.request.data['first_name'],
                                                  password=self.request.data['password'], is_amazon_admin=True)
            admin_query = serializer.save(user=user_query)
            print(admin_query)
            register_query = amazon_admin_notification.objects.create(amazon_admin=admin_query)
            Admin_query = serializer.save(amazon_admin_notification=register_query)
            print(Admin_query)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'status': 403, 'errors': serializer.errors, 'message': 'something went wrong'})


class adminapilist(RetrieveUpdateAPIView):
    queryset = Amazon_Admin.objects.all()
    serializer_class = admin_serializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query = self.request.user
        print(query.id)
        admin_detail = Amazon_Admin.objects.filter(user=query.id,Active=False)
        serializer = admin_serializer(admin_detail, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        query = self.request.user
        print(query.id)
        instance = Amazon_Admin.objects.get(user=query.id)
        print(instance.id)
        serializer = admin_serializer(instance, data=request.data)
        # print(serializers)
        if serializer.is_valid(raise_exception=True):
            message = "your profile is updated"
            Query = amazon_admin_notification.objects.create(amazon_admin=instance, message=message)
            serializer.save()
            # update_query = amazon_admin_notification.objects.create(message='your profile is updated ')
            # updated_query = serializer.save(amazon_admin_notification=update_query)
            # print(updated_query)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors)


class notificationlist(ListAPIView):
    queryset = amazon_admin_notification.objects.all()
    serializer_class = Amazon_Admin_Notificartions_Serializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def list(self, request, *args, **kwargs):
        query = (self.request.user)
        print(query.id)
        Query = amazon_admin_notification.objects.filter(amazon_admin=query.id)
        Query.update(seen=True,updated_at=datetime.datetime.now(), created_at =datetime.datetime.now())
        serializer = Amazon_Admin_Notificartions_Serializer(Query, many=True)
        return Response(serializer.data)


class countunseen_notification(ListAPIView):
    queryset = amazon_admin_notification.objects.all()
    serializer_class = Amazon_Admin_Notificartions_Serializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        query = (self.request.user)
        Query = amazon_admin_notification.objects.filter(amazon_admin=query.id,seen=False).count()
        print(Query)
        return Response({"count":Query})
class checksuperuserapi(RetrieveUpdateAPIView):
    queryset = Amazon_Admin.objects.all()
    serializer_class = admin_serializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
                admin_detail = Amazon_Admin.objects.filter(user=self.kwargs["pk"])
                serializer = admin_serializer(admin_detail, many=True)
                print(admin_detail)
                return Response(serializer.data)
        else:
                return Response("YOU ARE NOT SUPER USER")
    def update(self, request, *args, **kwargs):
        #query = self.request.user
       # print(query.id)
        instance = Amazon_Admin.objects.get(user=self.kwargs["pk"])
        #print(instance.id)
        serializer = checksuperuserapiserializer(instance,data=request.data)
        # print(serializers)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            query = self.request.data['Active']
            if query == 'True':
                amazon_admin_notification.objects.create(amazon_admin=instance, message="your account is activated")
            else:
                amazon_admin_notification.objects.create(amazon_admin=instance, message="your account is not activated")

            return Response(serializer.data, status=status.HTTP_200_OK)

            #print(active)

               # Query = amazon_admin_notification.objects.create(amazon_admin=instance,message="your account is activated")
            #lse:
              #  Query = amazon_admin_notification.objects.create(amazon_admin=instance,message="your account is not active")

        else:
             return Response({"NO_ACCESS": "Access Denied"}, status=status.HTTP_401_UNAUTHORIZED)
#