from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin
from . import views


app_name = 'accounts'


urlpatterns = [
    path('api/get_user/', views.get_logged_in_user, name='login_user_api'),
    path('register/', views.registration_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('', views.home, name="home"),
    path('tasks/<slug:category>', views.home, name="categories"),
    path('tasks/<slug:category>/<str:task_uuid>', views.home, name="tasks"),
    path('profile', views.home, name="home"),
]
