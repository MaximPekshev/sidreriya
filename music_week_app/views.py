from django.shortcuts import render
import datetime
from .models import MusicWeek

def show_actual_music_week(request):
    music_week = MusicWeek.objects.filter(date__lte=datetime.datetime.now()).order_by('date').last()
    context = {
        'music_week': music_week,
	}
    return  render(request, 'music_week_app/actual_music_week.html', context)