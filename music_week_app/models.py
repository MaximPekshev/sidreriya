from django.db import models

def get_image_name_without_slug(instance, filename):
	
	new_name = ('music_week_' + '%s' + '.' + filename.split('.')[-1]) % instance.date
	return new_name

class MusicWeek(models.Model):

	date	= models.DateField(unique=True ,verbose_name='Действует с:', auto_now=False, auto_now_add=False)
	image	= models.ImageField(upload_to=get_image_name_without_slug, verbose_name='Изображение 1280х904', default=None)

	class Meta:
		
		verbose_name = 'Музыкальная неделя'
		verbose_name_plural = 'Музыкальные недели'