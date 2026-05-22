from django.db import models
from baseapp.services import (
    get_image_name_by_slug, 
    get_uuid 
)

class DishesType(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование', blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Тип блюда'
        verbose_name_plural = 'Типы блюд'
    
class Dish(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование', blank=True)
    slug = models.SlugField(max_length=36, verbose_name='Url', blank=True, db_index=True)
    dish_type = models.ForeignKey(DishesType, on_delete=models.CASCADE, verbose_name='Тип блюда')
    description = models.TextField(verbose_name='Описание', blank=True)
    picture = models.ImageField(upload_to=get_image_name_by_slug, verbose_name='Изображение', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_uuid()
        super().save(*args, **kwargs)

class ObjectForSetLunch(models.Model):
    dish_type = models.ForeignKey(DishesType, on_delete=models.CASCADE, verbose_name='Тип блюда')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Блюдо')
    lunch_set = models.ForeignKey('LunchSet', on_delete=models.CASCADE, verbose_name='Комплексный обед')

    def __str__(self):
        return f'{self.dish.title} - {self.lunch_set.date}'

class LunchSet(models.Model):
    date = models.DateField(verbose_name='Дата', unique=True)
    comment = models.TextField(verbose_name='Комментарий', blank=True)

    def __str__(self):
        return f'Комплексный обед на {self.date}'
    
    class Meta:
        verbose_name = 'Комплексный обед'
        verbose_name_plural = 'Комплексные обеды'