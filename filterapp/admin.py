from django.contrib import admin

from .models import PropertiesFilter


class PropertiesFilterAdmin(admin.ModelAdmin):

	list_display = (
					'p_filter',
					)
	
admin.site.register(PropertiesFilter, PropertiesFilterAdmin)