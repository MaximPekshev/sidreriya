from django.contrib import admin

from .models import MusicWeek

class MusicWeekAdmin(admin.ModelAdmin):
	list_display = (
					'date',
					)

admin.site.register(MusicWeek, MusicWeekAdmin)
