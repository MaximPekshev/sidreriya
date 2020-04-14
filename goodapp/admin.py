from django.contrib import admin
from django import forms

from .models import Good, Picture, Properties, Property_value
from .models import Properties, Property_value
from .models import Object_property_values


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
					)
	
	inlines 	 = [PictureInline, Object_property_valuesInline, ]

	exclude = ('slug',)

admin.site.register(Good, GoodAdmin)


class PropertiesAdmin(admin.ModelAdmin):
	list_display = (
					'title',
					)
	
	inlines 	 = [Property_valueInline]

	exclude = ('slug',)

admin.site.register(Properties, PropertiesAdmin)


class Object_property_valuesAdmin(admin.ModelAdmin):
	form = Object_property_valuesInlineForm

	list_display = (
					'good',
					'_property',
					'property_value',
					)
	
	list_filter = 	(
					'good',
					)

admin.site.register(Object_property_values, Object_property_valuesAdmin)