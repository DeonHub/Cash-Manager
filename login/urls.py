# from django import views
from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.login, name="login"),
    path('login/', views.logins, name="logins"),
    path('index/', views.index, name="index"),

]