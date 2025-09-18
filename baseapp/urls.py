from django.urls import path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from baseapp.views import (
    IndexView,
    DeliveryView,
    AtmosphereView,
    AboutUsView,
    PromoView,
    SetLunchView,
    # GiftBoxesView,
    BreakfastView,
    CertificateView,
)

app_name = "baseapp"

urlpatterns = [
	path('', IndexView.as_view(), name='index'),
	path('delivery/', DeliveryView.as_view(), name='delivery'),
	path('atmosphere/', 	AtmosphereView.as_view(), name='atmosphere'),
	path('about-us/', 		AboutUsView.as_view(), name='about_us'),
	path('promo/', 			PromoView.as_view(), name='promo'),
	path('lunch-set/', 		SetLunchView.as_view(), name='set_lunch'),
	# path('gift-boxes/', 	GiftBoxesView.as_view(), name='gift_boxes'),
	path('breakfasts/', 	BreakfastView.as_view(), name='breakfasts'),
	path('certificate/', 	CertificateView.as_view(), name='сertificate'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()


