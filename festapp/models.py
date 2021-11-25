from django.db import models
import uuid
from uuslug import slugify

def get_uuid():
	return str(uuid.uuid4().fields[0])

def get_image_name(instance, filename):
	
	new_name = ('%s' + '.' + filename.split('.')[-1]) % instance.slug
	return new_name

class Festival(models.Model):

	name 				= models.CharField(max_length = 150, verbose_name='Наименование')
	description 		= models.TextField(max_length=2048, verbose_name='Описание', blank=True)
	meta_title 			= models.CharField(max_length=150, verbose_name='meta name', blank=True, null=True)
	meta_description 	= models.TextField(max_length=1024, verbose_name='meta description', blank=True, null=True)
	slug 				= models.SlugField(max_length=36, verbose_name='Url', blank=True, db_index=True)
	cpu_slug			= models.SlugField(max_length=70, verbose_name='ЧПУ_Url', blank=True, db_index=True)
	is_active			= models.BooleanField(verbose_name='Активен', default=False)
	menu_img			= models.ImageField(upload_to=get_image_name, verbose_name='Изображение меню 1545x2000', default=None, null=True, blank=True)
	list_img			= models.ImageField(upload_to=get_image_name, verbose_name='Изображение баннера 780x411', default=None, null=True, blank=True)
	color 				= models.CharField(max_length=7, verbose_name='Цвет согласно HEX, с решеткой', blank=True, null=True)


	def __str__(self):

		return self.name

	def save(self, *args, **kwargs):

		if self.slug == "":
			self.slug = get_uuid()

		self.cpu_slug = '{}'.format(slugify(self.name))	

		super(Festival, self).save(*args, **kwargs)

	class Meta:
		verbose_name = 'Фестиваль'
		verbose_name_plural = 'Фестивали'
