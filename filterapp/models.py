from django.db import models

from goodapp.models import Properties, Category

class PropertiesFilter(models.Model):
	
	p_filter = models.ForeignKey('goodapp.Properties', verbose_name='Фильтр по свойствам', on_delete=models.CASCADE)
	category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, default=None, null=True, blank=True)

	def __str__(self):
		
		return self.p_filter.title

	class Meta:
		verbose_name = 'Фильтр по свойствам'
		verbose_name_plural = 'Фильтры по свойствам'	
		