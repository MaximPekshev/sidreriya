from django.db import models


import os

from django.conf import settings

import uuid

from uuslug import slugify

def get_uuid():
	return str(uuid.uuid4().fields[0])


class Good(models.Model):

	name 				= models.CharField(max_length = 150, verbose_name='Наименование')
	name_en				= models.CharField(max_length = 150, verbose_name='Наименование на английском', blank=True,)
	description 		= models.TextField(max_length=2048, verbose_name='Описание', blank=True)

	gastronomy			= models.TextField(max_length=512, verbose_name='Гастрономия', blank=True, default='')

	meta_name 			= models.CharField(max_length=150, verbose_name='meta name', blank=True, null=True)
	meta_description 	= models.TextField(max_length=1024, verbose_name='meta description', blank=True, null=True)

	price 				= models.DecimalField(verbose_name='Цена', max_digits=15, decimal_places=0, blank=True, null=True)
	old_price			= models.DecimalField(verbose_name='Старая цена', max_digits=15, decimal_places=0, blank=True, null=True)

	is_active			= models.BooleanField(verbose_name='Активен', default=False)

	quantity			= models.DecimalField(verbose_name='Остаток', max_digits=15, decimal_places=0, blank=True, null=True)
	weight				= models.CharField(max_length = 36, verbose_name='Вес', blank=True, null=True, default='')
	
	good_uid 			= models.CharField(max_length=36, verbose_name='Код', blank=True, null=True)
	slug 				= models.SlugField(max_length=36, verbose_name='Url', blank=True, db_index=True)

	cpu_slug			= models.SlugField(max_length=70, verbose_name='ЧПУ_Url', blank=True, db_index=True)

	manufacturer 		= models.ForeignKey('Manufacturer', verbose_name='Производитель', on_delete=models.SET_DEFAULT,null=True, blank=True, default=None)

	category 			= models.ForeignKey('Category', verbose_name='Категория', on_delete=models.SET_DEFAULT,null=True, blank=True, default=None)

	in_barrel 			= models.BooleanField(verbose_name='Розлив', default=False)

	def __str__(self):

		return self.name

	def save(self, *args, **kwargs):

		if self.slug == "":
			self.slug = get_uuid()

		self.cpu_slug = '{}'.format(slugify(self.name_en if self.name_en else self.name))	

		super(Good, self).save(*args, **kwargs)
			
	
	class Meta:
		verbose_name = 'Товар'
		verbose_name_plural = 'Товары'


class Manufacturer(models.Model):

	name 				= models.CharField(max_length = 150, verbose_name='Наименование')
	name_en				= models.CharField(max_length = 150, verbose_name='Наименование на английском', blank=True,)
	description 		= models.TextField(max_length=2048, verbose_name='Описание', blank=True)

	meta_name 			= models.CharField(max_length=150, verbose_name='meta name', blank=True, null=True)
	meta_description 	= models.TextField(max_length=1024, verbose_name='meta description', blank=True, null=True)

	slug 				= models.SlugField(max_length=36, verbose_name='Url', blank=True, db_index=True)

	cpu_slug			= models.SlugField(max_length=70, verbose_name='ЧПУ_Url', blank=True, db_index=True)
		
	def __str__(self):

		return self.name

	def save(self, *args, **kwargs):

		if self.slug == "":
			self.slug = get_uuid()

		self.cpu_slug = '{}'.format(slugify(self.name_en if self.name_en else self.name))	

		super(Manufacturer, self).save(*args, **kwargs)

	class Meta:
		verbose_name = 'Производитель'
		verbose_name_plural = 'Производители'


def get_image_name(instance, filename):
	
	new_name = ('%s' + '.' + filename.split('.')[-1]) % instance.slug
	return new_name

class Category(models.Model):

	name 				= models.CharField(max_length = 150, verbose_name='Наименование')
	meta_name 			= models.CharField(max_length=150, verbose_name='meta name', blank=True, null=True)
	meta_description 	= models.TextField(max_length=1024, verbose_name='meta description', blank=True, null=True)

	slug 				= models.SlugField(max_length=36, verbose_name='Url', blank=True, db_index=True)
	cpu_slug			= models.SlugField(max_length=70, verbose_name='ЧПУ_Url', blank=True, db_index=True)
	parent_category 	= models.ForeignKey('Category', verbose_name='Категория', on_delete=models.SET_DEFAULT,null=True, blank=True, default=None)
	picture				= models.ImageField(upload_to=get_image_name, verbose_name='Изображение 370x334', default=None, null=True, blank=True)

	rank				= models.DecimalField(verbose_name='Порядок', max_digits=6, decimal_places=0, blank=True, null=True)


	def __str__(self):

		return self.name

	def save(self, *args, **kwargs):

		if self.slug == "":
			self.slug = get_uuid()

		self.cpu_slug = '{}'.format(slugify(self.name))	

		super(Category, self).save(*args, **kwargs)

	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'		
	


class Picture(models.Model):

	title 					= models.CharField(max_length=150, verbose_name='Наименование', blank=True)
	slug 					= models.SlugField(max_length=36, verbose_name='Url', blank=True, db_index=True)
	good 					= models.ForeignKey('Good', verbose_name='Товар', on_delete=models.CASCADE)
	images					= models.ImageField(upload_to=get_image_name, verbose_name='Изображение 550x685', default=None)
	
	main_image				= models.BooleanField(verbose_name='Основная картинка', default=False)

	def __str__(self):
		
		return self.slug

	def save(self, *args, **kwargs):
		
		if self.slug == "":
			self.slug = get_uuid()
			self.title = self.slug

		super(Picture, self).save(*args, **kwargs)


	

	class Meta:
		
		verbose_name = 'Картинка'
		verbose_name_plural = 'Картинки'

class Properties(models.Model):

	title 					= models.CharField(max_length=150, verbose_name='Наименование', blank=True)
	slug 					= models.SlugField(max_length=36, verbose_name='Url', blank=True, db_index=True)

	def __str__(self):
		
		return self.title

	def save(self, *args, **kwargs):
		
		if self.slug == "":
			self.slug = get_uuid()

		super(Properties, self).save(*args, **kwargs)


	class Meta:
		
		verbose_name = 'Свойство'
		verbose_name_plural = 'Свойства'


class Property_value(models.Model):

	title 					= models.CharField(max_length=150, verbose_name='Наименование', blank=True)
	slug 					= models.SlugField(max_length=36, verbose_name='Url', blank=True, db_index=True)
	_property				= models.ForeignKey('Properties', verbose_name='Свойства', on_delete=models.CASCADE)

	def __str__(self):
		
		return self.title

	def save(self, *args, **kwargs):
		
		if self.slug == "":
			self.slug = get_uuid()

		super(Property_value, self).save(*args, **kwargs)


	class Meta:
		
		verbose_name = 'Значение свойства'
		verbose_name_plural = 'Значения свойства'


class Object_property_values(models.Model):

	good					= models.ForeignKey('Good', verbose_name='Товар', on_delete=models.CASCADE)
	_property 				= models.ForeignKey('Properties', verbose_name='Свойство', on_delete=models.CASCADE)
	property_value 			= models.ForeignKey('Property_value', verbose_name='Значение', on_delete=models.CASCADE, blank=True, null=True)
	

	class Meta:
		
		verbose_name = 'Значение свойств объекта'
		verbose_name_plural = 'Значения свойств объекта'

		unique_together = (('good', '_property'),)
		

class In_Barrels(models.Model):

	good					= models.ForeignKey('Good', verbose_name='Товар', on_delete=models.CASCADE)

	class Meta:
		
		verbose_name = 'Сидр в бочках'
		verbose_name_plural = 'Сидры в бочках'
	