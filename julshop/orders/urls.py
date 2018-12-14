from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [

    url(r'^cart_adding/', views.cart_adding, name='cart_adding'),
]