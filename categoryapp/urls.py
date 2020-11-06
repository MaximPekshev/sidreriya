from django.urls import path
from django.contrib import admin
from goodapp.views import show_category

urlpatterns = [

	path('<str:slug>/', 		show_category, name='show_category'),

			]