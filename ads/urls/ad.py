from django.urls import path

import ads.views

urlpatterns = [
    path('', ads.views.AdListView.as_view()),
    path('create/', ads.views.AdCreateView.as_view()),
    path('<int:pk>/', ads.views.AdDetailView.as_view()),
    path('<int:pk>/delete/', ads.views.AdDeleteView.as_view()),
    path('<int:pk>/update/', ads.views.AdUpdateView.as_view()),
]
