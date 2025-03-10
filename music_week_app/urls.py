from django.urls import path
from .views import MusicWeekView

urlpatterns = [
	path('', MusicWeekView.as_view(), name='show_actual_music_week'),
]