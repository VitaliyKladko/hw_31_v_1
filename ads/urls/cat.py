from django.urls import path

import ads.views

urlpatterns = [
    path('', ads.views.CategoryListView.as_view()),
    path('<int:pk>/', ads.views.CategoryDetailView.as_view()),
    path('<int:pk>/update/', ads.views.CategoryUpdateView.as_view()),
    path('<int:pk>/delete/', ads.views.CategoryDeleteView.as_view()),
    path('create/', ads.views.CategoryCreateView.as_view()),
]