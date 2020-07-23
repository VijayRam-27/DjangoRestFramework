from django.urls import path, include
from rest_framework import routers
from .import views


urlpatterns = [
    path('post_save', views.PostRegistrationView.as_view()),
    path('post_get/<int:pk>', views.GetRegistrationView.as_view())
]