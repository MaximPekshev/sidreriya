from django.urls import path
from django.contrib import admin
from goodapp.views import show_manufacturer

urlpatterns = [

	path('<str:slug>/', 		show_manufacturer, name='show_manufacturer'),

			]