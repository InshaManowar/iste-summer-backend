from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin
from . import views

app_name = 'course'

urlpatterns = [
    path('get_categories/', views.category_view, name='category'),
    path('get_tasks/<slug:slug>', views.task_view, name='task'),
    path('profile/', views.profile_view, name='profile'),
    path('upload/', views.submission, name='submit'),
    path('get_certificate/<slug:category_slug>',
         views.get_certificate, name="get_certificate"),
]
