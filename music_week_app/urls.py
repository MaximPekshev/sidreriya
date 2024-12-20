from django.urls import path
from .views import show_actual_music_week

urlpatterns = [
	path('', show_actual_music_week, name='show_actual_music_week'),
]