from django.db import models

from goodapp.models import Properties

class PropertiesFilter(models.Model):
	
	p_filter = models.ForeignKey('goodapp.Properties', verbose_name='Фильтр по свойствам', on_delete=models.CASCADE)

	def __str__(self):
		
		return self.p_filter.title
		