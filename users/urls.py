from django.urls import path

import users.views

urlpatterns = [
    path('', users.views.UserListView.as_view()),
    path('create/', users.views.UserCreateView.as_view()),
    path('<int:pk>/', users.views.UserDetailView.as_view()),
    path('<int:pk>/update/', users.views.UserUpdateView.as_view()),
    path('<int:pk>/delete/', users.views.UserDeleteView.as_view()),
]
