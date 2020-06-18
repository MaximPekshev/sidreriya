from django.contrib import admin
from django import forms

from django.utils.safestring import mark_safe

import csv
from django.http import HttpResponse


from .models import Good, Picture
from .models import Properties, Property_value
from .models import Object_property_values
from .models import Manufacturer, Category, In_Barrels


class Object_property_valuesInlineForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(Object_property_valuesInlineForm, self).__init__(*args, **kwargs)
		try:
			self.fields['property_value'].queryset = Property_value.objects.filter(_property=self.instance._property)
		except:
			self.fields['property_value'].queryset = Property_value.objects
		


class PictureInline(admin.TabularInline):
    model = Picture

    fields = (
    			'images',
    			'main_image',
    	)

    exclude = ('title', 'slug')
    extra = 0


class Property_valueInline(admin.TabularInline):
    model = Property_value
    exclude = ('slug',)
    extra = 0

class Object_property_valuesInline(admin.TabularInline):
	form = Object_property_valuesInlineForm
	model = Object_property_values
	extra = 0


class GoodAdmin(admin.ModelAdmin):
	list_display = (
					'name',
					'name_en',
					'good_uid',
					'price',
					'quantity',
					'weight',
					'is_active',
					'category',
					'manufacturer',
					'image',
					)

	list_filter = ('category', 'manufacturer')

	inlines 	 = [PictureInline, Object_property_valuesInline, ]

	actions = ["export_as_csv"]

	exclude = ('slug',)

	def formfield_for_foreignkey(self, db_field, request, **kwargs):

		if db_field.name == "manufacturer":
			kwargs["queryset"] = Manufacturer.objects.all()
			return super(GoodAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

		if db_field.name == "category":
			kwargs["queryset"] = Category.objects.all()
			return super(GoodAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

	def image(self, obj):

		img = Picture.objects.filter(good=obj, main_image=True).first() if Picture.objects.filter(good=obj, main_image=True).first() else Picture.objects.filter(good=obj).first()
		if img:
			return mark_safe('<img src="{url}" width="50" />'.format(url=img.images.url))
		else:
			return ''	

	def export_as_csv(self, request, queryset):

		meta = self.model._meta
		field_names = [field.name for field in meta.fields]
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
		writer = csv.writer(response)

		writer.writerow(field_names)
		for obj in queryset:
			row = writer.writerow([getattr(obj, field) for field in field_names])

		return response

	export_as_csv.short_description = "Выгрузить выбранные"

admin.site.register(Good, GoodAdmin)




class PropertiesAdmin(admin.ModelAdmin):
	list_display = (
					'title',
					)
	
	inlines 	 = [Property_valueInline]

	exclude = ('slug',)

admin.site.register(Properties, PropertiesAdmin)

class ManufacturerAdmin(admin.ModelAdmin):
	list_display = (
					'name',
					)
	
	exclude = ('slug',)

admin.site.register(Manufacturer, ManufacturerAdmin)

class CategoryAdmin(admin.ModelAdmin):
	list_display = (
					'name',
					'rank',
					)
	
	exclude = ('slug',)

admin.site.register(Category, CategoryAdmin)

class In_BarrelsAdmin(admin.ModelAdmin):
	list_display = (
					'good',
					)

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == "good":
			kwargs["queryset"] = Good.objects.filter(in_barrel=True)
		return super(In_BarrelsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
	
admin.site.register(In_Barrels, In_BarrelsAdmin)
