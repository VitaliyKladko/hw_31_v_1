import json

from django.core.paginator import Paginator
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ads.models import Category, Ad
from hw_28_v3 import settings
from users.models import User


class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = []
        for cat in self.object_list:
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
        all_ads = Ad.objects.all()

        paginator = Paginator(all_ads, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        response = {
            'items': [ad.serialize() for ad in page_obj],
            'total_pages': paginator.num_pages,
            'total_elements': paginator.count
        }

        return JsonResponse(response, status=200)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except Http404:
            return JsonResponse({'error': 'Not Found'}, status=404)

        return JsonResponse(ad.serialize(), status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ['name', 'author', 'price', 'description', 'category', 'is_published']

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        author = get_object_or_404(User, pk=ad_data.pop('author'))
        category = get_object_or_404(Category, pk=ad_data.pop('category'))

        ad = Ad.objects.create(author=author, category=category, **ad_data)

        return JsonResponse(ad.serialize(), status=201)


# Здесь должен быть апдейт вью
@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ['name', 'author', 'price', 'description', 'category', 'is_published']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_update_data = json.loads(request.body)

        if 'name' in ad_update_data:
            self.object.name = ad_update_data['name']

        if 'author' in ad_update_data:
            self.object.author = get_object_or_404(User, pk=ad_update_data['author'])

        if 'price' in ad_update_data:
            self.object.price = ad_update_data['price']

        if 'description' in ad_update_data:
            self.object.description = ad_update_data['description']

        if 'category' in ad_update_data:
            self.object.category = get_object_or_404(Category, pk=ad_update_data['category'])

        if 'is_published' in ad_update_data:
            self.object.is_published = ad_update_data['is_published']

        return JsonResponse(self.object.serialize(), status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({
            'status': 'Ok'
        }, status=200)
