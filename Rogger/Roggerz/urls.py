from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.extract, name='home'),  
    path('Roggerz/', views.extract, name='roggerz'),  

]
    