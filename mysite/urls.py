from django.contrib import admin
from django.urls import path
from career_finder import views  # Import the views from career_finder

urlpatterns = [
    path('', views.index, name='index'),
    path('role_call/', views.role_call, name='role_call'),  # Make sure the function name matches
            path('start_scraping/', views.start_scraping, name='start_scraping'),
             path('fetch_companies/', views.fetch_companies_data, name='fetch_companies_data'),
]