from django.urls import path
from django.urls import include
from .views import show_festival_list
from .views import show_festival

urlpatterns = [
	path('', 			show_festival_list, name='show_festival_list'),
	path('<str:cpu_slug>/', show_festival, name='show_festival'),
]