from django.contrib import admin

from .models import Good, Picture


class PictureInline(admin.TabularInline):
    model = Picture
    exclude = ('title', 'slug')
    extra = 0

class GoodAdmin(admin.ModelAdmin):
	list_display = (
					'name',
					'name_en',
					'good_uid',
					'price',
					'quantity',
					'is_active',
					)
	
	inlines 	 = [PictureInline]

	exclude = ('slug',)

admin.site.register(Good, GoodAdmin)
