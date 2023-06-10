from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from ads.models import Category, Ad, Selection
from ads.permissions import IsOwner, IsAdOwner, IsStaff
from ads.serializers import AdRetrieveViewSerializer, SelectionSerializer, SelectionCreateSerializer, \
    AdUpdateSerializer, AdDestroyView, AdCreateAPIViewSerializer, CategoryViewSetSerializer, AdListSerializer
from users.models import User


@extend_schema_view(list=extend_schema(description="Retrieve Category (подробное опис.)", summary="Category list"),)
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryViewSetSerializer


class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdListSerializer


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
