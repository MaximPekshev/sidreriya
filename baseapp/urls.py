from django.urls import path
from django.contrib import admin

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from .views import show_index
from .views import show_delivery
from .views import show_atmosphere
from .views import show_about_us
from .views import show_contact_us
from .views import show_promo
from .views import show_set_lunch
from .views import show_gift_boxes
from .views import show_breakfasts
from .views import show_сertificate


urlpatterns = [

	path('', 				show_index, name='show_index'),
	path('delivery/', 		show_delivery, name='show_delivery'),
	path('atmosphere/', 	show_atmosphere, name='show_atmosphere'),
	path('about-us/', 		show_about_us, name='show_about_us'),
	path('contact-us/', 	show_contact_us, name='show_contact_us'),
	path('promo/', 			show_promo, name='show_promo'),
	path('lunch-set/', 		show_set_lunch, name='show_set_lunch'),
	path('gift-boxes/', 	show_gift_boxes, name='show_gift_boxes'),
	path('breakfasts/', 	show_breakfasts, name='show_breakfasts'),
	path('certificate/', 	show_сertificate, name='show_сertificate'),


			]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()


