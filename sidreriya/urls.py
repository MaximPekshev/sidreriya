from django.contrib import admin
from django.urls import path
from django.urls import include
from goodapp.views import sitemap_xml_view
admin.autodiscover()

urlpatterns = [
	path('', include('baseapp.urls')),
    path('sitemap.xml', sitemap_xml_view, name='sitemap_xml'),
	path('catalog/', include('goodapp.urls')),
    path('accounts/', include('authapp.urls')),
    path('cart/', include('cartapp.urls')),
    path('order/', include('orderapp.urls')),
    path('wishlist/', include('wishlistapp.urls')),
    path('fest/', include('festapp.urls')),
    path('music-events/', include('music_week_app.urls')),
    path('api/v1/', include('api_app.urls')),
    path('api/v2/', include('API.urls')),
    path('admin/', admin.site.urls),
]
