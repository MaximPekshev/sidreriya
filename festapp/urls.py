from django.urls import path
from .views import (
    FestivalListView,
    FestivalView,
)

urlpatterns = [
	path('', FestivalListView.as_view(), name='show_festival_list'),
	path('<str:cpu_slug>/', FestivalView.as_view(), name='show_festival'),
]