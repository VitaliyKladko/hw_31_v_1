import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView

from hw_28_v3 import settings
from users.models import User, Location
from users.serializers import UserListViewSerializer, UserRetrieveViewSerializer, UserCreateAPIViewSerializer, \
    UserUpdateAPIViewSerializer


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


# class UserListView(ListView):
#     queryset = User.objects.annotate(total_ads=Count('ad', filter=Q(ad__is_published=True)))
#
#     def get(self, request, *args, **kwargs):
#         super().get(request, *args, **kwargs)
#
#         paginator = Paginator(self.object_list.order_by('username'), settings.TOTAL_ON_PAGE)
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
#
#         response = {
#             'items': [{**user.serialize(), 'total_ads': user.total_ads} for user in page_obj],
#             'total_pages': paginator.num_pages,
#             'total_elements': paginator.count
#         }
#
#         return JsonResponse(response, status=200)


# class UserDetailView(DetailView):
#     model = User
#
#     def get(self, request, *args, **kwargs):
#         try:
#             user = self.get_object()
#         except Http404:
#             return JsonResponse({'error': 'Not Found'}, status=404)
#
#         return JsonResponse(user.serialize(), status=200)


# @method_decorator(csrf_exempt, name='dispatch')
# class UserCreateView(CreateView):
#     model = User
#     fields = ['username', 'password', 'first_name', 'last_name', 'role', 'age', 'locations']
#
#     def post(self, request, *args, **kwargs):
#         user_data = json.loads(request.body)
#
#         locations = user_data.pop('locations')
#         user = User.objects.create(**user_data)
#         for loc_name in locations:
#
#             loc, _ = Location.objects.get_or_create(name=loc_name)
#             user.locations.add(loc)
#
#         return JsonResponse(user.serialize(), status=201)


# @method_decorator(csrf_exempt, name='dispatch')
# class UserUpdateView(UpdateView):
#     model = User
#     fields = ['username', 'password', 'first_name', 'last_name', 'age', 'locations']
#
#     def patch(self, request, *args, **kwargs):
#         super().post(request, *args, **kwargs)
#
#         user_update_data = json.loads(request.body)
#
#         if 'username' in user_update_data:
#             self.object.username = user_update_data['username']
#
#         if 'password' in user_update_data:
#             self.object.password = user_update_data['password']
#
#         if 'first_name' in user_update_data:
#             self.object.first_name = user_update_data['first_name']
#
#         if 'last_name' in user_update_data:
#             self.object.last_name = user_update_data['last_name']
#
#         if 'age' in user_update_data:
#             self.object.age = user_update_data['age']
#
#         if 'locations' in user_update_data:
#             locations = user_update_data.pop('locations')
#             self.object.locations.clear()  # метод очистит связи между User и Location
#             for loc_name in locations:
#                 loc, _ = Location.objects.get_or_create(name=loc_name)
#                 self.object.locations.add(loc)
#
#         self.object.save()
#
#         return JsonResponse(self.object.serialize(), status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({
            'status': 'Ok'
        }, status=200)
