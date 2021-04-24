from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin
from . import views


app_name='accounts'

urlpatterns = [
    path('api/get_user/', views.get_logged_in_user, name='login_user_api'),
    path('register/', views.registration_view, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.login_view, name='logout'),
    
    
]



