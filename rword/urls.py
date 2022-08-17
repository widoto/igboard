from django.urls import path
from . import views

urlpatterns = [
    path('', views.rwordpage, name='rwordpage'),
    path('rboard/', views.rwordboard, name='rwordboard'),
    path('rboard/detail/<int:pk>', views.rword_detail, name='rword_detail'),
]