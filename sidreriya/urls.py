from django.contrib import admin
from django.urls import path
from django.urls import include
# from ajax_select import urls as ajax_select_urls

admin.autodiscover()

urlpatterns = [
	path(''		 		, include('baseapp.urls')),
	path('catalog/'		, include('goodapp.urls')),
    path('accounts/'    , include('authapp.urls')),
    path('cart/'        , include('cartapp.urls')),
    path('order/'       , include('orderapp.urls')),
    path('wishlist/'    , include('wishlistapp.urls')),
    path('fest/'        , include('festapp.urls')),
    path('music-events/'  , include('music_week_app.urls')),
    # path('API/'    		, include('API.urls')),
    # path('ajax_select/', include(ajax_select_urls)),
    path('admin/'		, admin.site.urls),

]
