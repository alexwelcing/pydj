from django.contrib import admin
from django.urls import path
from career_finder import views  # Import the views from career_finder

urlpatterns = [
    path('', views.index, name='index'),
    ]