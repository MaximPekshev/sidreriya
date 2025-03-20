from django.shortcuts import render
from django.views.generic import View
from datetime import datetime
from music_week_app.models import MusicWeek

class MusicWeekView(View):
    
    def get(self, request):
        music_week = MusicWeek.objects.filter(date__lte=datetime.now()).order_by('date').last()
        context = {
            'music_week': music_week,
        }
        return  render(request, 'music_week_app/actual_music_week.html', context)