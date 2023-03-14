from django.contrib import admin

from .models import PropertiesFilter


class PropertiesFilterAdmin(admin.ModelAdmin):

	list_display = (
					'p_filter',
					'category',
					)
	
admin.site.register(PropertiesFilter, PropertiesFilterAdmin)