import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

from hw_28_v3 import settings
from users.models import User, Location
from users.serializers import UserListViewSerializer, UserRetrieveViewSerializer, UserCreateAPIViewSerializer, \
    UserUpdateAPIViewSerializer, UserDestroyAPIViewSerializer, LocationSerializer


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListViewSerializer


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveViewSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateAPIViewSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateAPIViewSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDestroyAPIViewSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
