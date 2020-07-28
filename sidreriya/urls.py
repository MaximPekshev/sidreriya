from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
	path(''		 		, include('baseapp.urls')),
	path('catalog/'		, include('goodapp.urls')),
    path('accounts/'    , include('authapp.urls')),
    path('cart/'        , include('cartapp.urls')),
    path('order/'       , include('orderapp.urls')),
    path('wishlist/'    , include('wishlistapp.urls')),
    # path('API/'    		, include('API.urls')),
    path('admin/'		, admin.site.urls),
]
