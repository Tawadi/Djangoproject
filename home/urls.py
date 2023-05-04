from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('Home/', views.home, name="home"),
    path('about/', views.about, name='about'),
    path('project/', views.project, name='project'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout, name="logout"),
    path('search/', views.search, name="search"),
    path('cart/', views.cart, name="cart"),
    path('orders/', views.orders , name="orders"),
    path('success/', views.success, name="success")
    ]