from django.urls import path
from django.contrib import admin
from django.urls import include
from .views import show_catalog, show_good, show_in_barrels

urlpatterns = [

	path('', 						show_catalog, name='show_catalog'),
	path('in-barrels/', 			show_in_barrels, name='show_in_barrels'),
	path('category/', 				include('categoryapp.urls')),
	path('manufacturer/', 			include('manufacturerapp.urls')),
	path('<str:slug>/', 			show_good, name='show_good'),

			]