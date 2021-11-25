from django.contrib import admin

from .models import Festival


class FestivalAdmin(admin.ModelAdmin):
	list_display = (
					'name',
					'is_active',
					)
	
	exclude = ('slug', 'cpu_slug')

	search_fields = ('name', )

admin.site.register(Festival, FestivalAdmin)