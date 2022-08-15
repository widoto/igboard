from django.urls import path
from . import views

urlpatterns = [
    path('', views.rwordpage, name='rwordpage'),
    path('rboard/', views.rwordboard, name='rwordboard'),
]