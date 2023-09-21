from django.contrib import admin
from django.urls import path
from career_finder import views  # Import the views from career_finder

urlpatterns = [
    path('', views.index, name='index'),
    path('roll_call/', views.role_call, name='roll_call'),  # Make sure the function name matches
            path('start_scraping/', views.start_scraping, name='start_scraping'),
                path('fetch_companies/', views.fetch_companies, name='fetch_companies'),
    ]