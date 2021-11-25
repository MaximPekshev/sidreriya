from django.urls import path
from django.contrib import admin
from django.urls import include
from .views import show_catalog, show_good, show_in_barrels
from .views import show_product_with_tag, show_product_with_filters
from .views import show_search_result

urlpatterns = [
	path('', 						show_catalog, name='show_catalog'),
	path('search/', 				show_search_result, name='show_search_result'),
	path('show-tag/', 				show_product_with_tag, name='show_product_with_tag'),
	path('filter/', 				show_product_with_filters, name='show_product_with_filters'),
	path('in-barrels/', 			show_in_barrels, name='show_in_barrels'),
	path('category/', 				include('categoryapp.urls')),
	path('manufacturer/', 			include('manufacturerapp.urls')),
	path('<str:slug>/', 			show_good, name='show_good'),


			]