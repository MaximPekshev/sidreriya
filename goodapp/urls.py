from django.urls import path
from django.contrib import admin
from django.urls import include
from .views import show_catalog, show_good

urlpatterns = [

	path('', 						show_catalog, name='show_catalog'),
	path('category/', 				include('categoryapp.urls')),
	path('manufacturer/', 			include('manufacturerapp.urls')),
	path('<str:slug>/', 			show_good, name='show_good'),

			]