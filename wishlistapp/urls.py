from django.urls import path
from .views import WishlistView
from .views import wishlist_add_item

urlpatterns = [
	path('', WishlistView.as_view(), name='show_wishlist'),
	path('add/<str:slug>/', wishlist_add_item, name='wishlist_add_item'),
]