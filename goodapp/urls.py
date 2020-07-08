from django.urls import path
from django.contrib import admin
from django.urls import include
from .views import show_catalog, show_good, show_in_barrels
from .views import show_product_with_tag

urlpatterns = [

	path('', 						show_catalog, name='show_catalog'),
	path('filter/', 				show_product_with_tag, name='show_product_with_tag'),
	path('in-barrels/', 			show_in_barrels, name='show_in_barrels'),
	path('category/', 				include('categoryapp.urls')),
	path('manufacturer/', 			include('manufacturerapp.urls')),
	path('<str:slug>/', 			show_good, name='show_good'),

			]