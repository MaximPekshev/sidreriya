from django.contrib import admin
from django import forms
from django.http import HttpResponse
from django.utils.safestring import mark_safe

import csv

from goodapp.models import (
	Good,
	Picture,
	Properties,
	Property_value,
	Object_property_values,
	Manufacturer,
	Bestseller,
	Category,
	In_Barrels,
	Set_Lunch,
	Set_Meal,
	First_Course,
	Second_Course,
	Third_Course
)


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
					'slug',
					'price',
					'quantity',
					'weight',
					'is_active',
					'category',
					'manufacturer',
					'image',
					)

	list_filter = ('category', 'manufacturer')

	inlines 	 = [PictureInline, Object_property_valuesInline]

	actions = ["export_as_csv"]

	search_fields = ('name', 'name_en', )

	exclude = ('slug', 'cpu_slug')

	def formfield_for_foreignkey(self, db_field, request, **kwargs):

		if db_field.name == "manufacturer":
			kwargs["queryset"] = Manufacturer.objects.all()
			return super(GoodAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

		if db_field.name == "category":
			kwargs["queryset"] = Category.objects.all()
			return super(GoodAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
		
	def formfield_for_manytomany(self, db_field, request, **kwargs):
		
		if db_field.name == "upsell_products":
			kwargs["queryset"] = Good.objects.filter(is_active=True).order_by('name')
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
	
	exclude = ('slug', 'cpu_slug')

	search_fields = ('name', 'name_en', )

admin.site.register(Manufacturer, ManufacturerAdmin)

class CategoryAdmin(admin.ModelAdmin):
	list_display = (
					'name',
					'rank',
					)
	
	# exclude = ('slug', 'cpu_slug')
	exclude = ('cpu_slug',)

	search_fields = ('name', )

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

class First_Course_Form(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(First_Course_Form, self).__init__(*args, **kwargs)
		self.fields['good'].queryset = Good.objects.filter(category__name="Первое блюдо")

class Second_Course_Form(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(Second_Course_Form, self).__init__(*args, **kwargs)
		self.fields['good'].queryset = Good.objects.filter(category__name="Второе блюдо")

class Third_Course_Form(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(Third_Course_Form, self).__init__(*args, **kwargs)
		self.fields['good'].queryset = Good.objects.filter(category__name="Третье блюдо")

class First_CourseInline(admin.TabularInline):
	form = First_Course_Form
	model = First_Course
	extra = 0

class Second_CourseInline(admin.TabularInline):
	form = Second_Course_Form
	model = Second_Course
	extra = 0

class Third_CourseInline(admin.TabularInline):
	form = Third_Course_Form
	model = Third_Course
	extra = 0

class Set_MealAdmin(admin.ModelAdmin):
	list_display = (
					'date',
					)
	inlines 	 = [First_CourseInline, Second_CourseInline, Third_CourseInline]

admin.site.register(Set_Meal, Set_MealAdmin)

class Set_LunchAdmin(admin.ModelAdmin):
	list_display = (
					'date',
					'image',
					)
	
admin.site.register(Set_Lunch, Set_LunchAdmin)

class BestsellerAdmin(admin.ModelAdmin):
	list_display = (
					'good',
					)

	exclude = ('name',)

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == "good":
			kwargs["queryset"] = Good.objects.filter( is_active=True).order_by('name')
		return super(BestsellerAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
	
admin.site.register(Bestseller, BestsellerAdmin)