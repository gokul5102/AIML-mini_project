
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home,name='home'),
    path('predict', views.predict),
    path('register', views.register.as_view(),name='register'),
    path('login/', views.login.as_view(), name='login'),
     path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
]
