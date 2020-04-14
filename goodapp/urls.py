from django.urls import path
from django.contrib import admin
from .views import show_catalog, show_good

urlpatterns = [

	path('', 				show_catalog, name='show_catalog'),
	path('<str:slug>/', 	show_good, name='show_good'),

			]