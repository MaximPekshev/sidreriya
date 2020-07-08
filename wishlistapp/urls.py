from django.urls import path
from .views import show_wishlist
from .views import wishlist_add_item

urlpatterns = [
	path('', 		show_wishlist, name='show_wishlist'),
	path('add/<str:slug>/', wishlist_add_item, name='wishlist_add_item'),
]