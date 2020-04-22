from django.contrib import admin
from django import forms

from .models import Good, Picture
from .models import Properties, Property_value
from .models import Object_property_values
from .models import Manufacturer, Category


class Object_property_valuesInlineForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(Object_property_valuesInlineForm, self).__init__(*args, **kwargs)
		try:
			self.fields['property_value'].queryset = Property_value.objects.filter(_property=self.instance._property)
		except:
			self.fields['property_value'].queryset = Property_value.objects
		


class PictureInline(admin.TabularInline):
    model = Picture
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
					'is_active',
					'category',
					'manufacturer',
					)
	
	inlines 	 = [PictureInline, Object_property_valuesInline, ]

	exclude = ('slug',)

	def formfield_for_foreignkey(self, db_field, request, **kwargs):

		if db_field.name == "manufacturer":
			kwargs["queryset"] = Manufacturer.objects.all()
			return super(GoodAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

		if db_field.name == "category":
			kwargs["queryset"] = Category.objects.all()
			return super(GoodAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)	

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
					)
	
	exclude = ('slug',)

admin.site.register(Category, CategoryAdmin)
