import json

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from ads.models import Category, Ad, Selection
from ads.permissions import IsOwner, IsAdOwner, IsStaff
from ads.serializers import AdRetrieveViewSerializer, SelectionSerializer, SelectionCreateSerializer, \
    AdUpdateSerializer, AdDestroyView, AdCreateAPIViewSerializer
from hw_28_v3 import settings
from users.models import User


class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = []
        for cat in self.object_list.order_by('name'):
            response.append(cat.serialize())

        return JsonResponse(response, safe=False, status=200)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        try:
            category = self.get_object()
        except Http404:
            return JsonResponse({'error': 'Not Found'}, status=404)

        return JsonResponse(category.serialize(), status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        cat_data = json.loads(request.body)

        category = Category.objects.create(
            name=cat_data['name']
        )

        return JsonResponse(category.serialize(), status=201)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        cat_data = json.loads(request.body)

        self.object.name = cat_data['name']
        self.object.save()

        return JsonResponse(self.object.serialize(), status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({
            'status': 'Ok'
        }, status=200)


class AdListView(ListView):
    queryset = Ad.objects.order_by('-price')

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        # фильтрация ниже:
        search_category_id = request.GET.getlist('cat', None)
        category_q = None
        for cat in search_category_id:
            if category_q is None:
                category_q = Q(category__id=cat)
            else:
                category_q |= Q(category__id=cat)

        if category_q:
            self.queryset = self.queryset.filter(category_q)

        search_text = request.GET.get('text', None)
        if search_text:
            self.queryset = self.queryset.filter(name__icontains=search_text)

        search_location = request.GET.get('location', None)
        if search_location:
            self.queryset = self.queryset.filter(author__locations__name__icontains=search_location)

        price_from = request.GET.get('price_from', None)
        price_to = request.GET.get('price_to', None)
        if price_from and price_to:
            self.queryset = self.queryset.filter(price__range=[price_from, price_to])

        paginator = Paginator(self.queryset, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        response = {
            'items': [ad.serialize() for ad in page_obj],
            'total_pages': paginator.num_pages,
            'total_elements': paginator.count
        }

        return JsonResponse(response, safe=False, status=200)


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdRetrieveViewSerializer
    permission_classes = [IsAuthenticated]


class AdCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AdCreateAPIViewSerializer


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [IsAdOwner | IsStaff]


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDestroyView
    permission_classes = [IsAdOwner | IsStaff]


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = ['image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES['image']
        self.object.save()

        return JsonResponse(self.object.serialize(), status=200)


class SelectionViewSet(ModelViewSet):
    queryset = Selection.objects.all()
    serializers = {
        'create': SelectionCreateSerializer
    }
    default_serializer = SelectionSerializer
    permission = {
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated],
        'update': [IsOwner],
        'destroy': [IsOwner],
        'partial_update': [IsOwner]
    }
    default_permission = [AllowAny]

    def get_permissions(self):
        self.permission_classes = self.permission.get(self.action, self.default_permission)
        return super().get_permissions()

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)
