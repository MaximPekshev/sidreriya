from django.db import models
from PIL import Image

from baseapp.services import (
    get_image_name_by_slug, 
    get_uuid 
)

class Breakfast(models.Model):
    slug = models.SlugField(max_length=36, verbose_name='Slug', blank=True, db_index=True) 
    image = models.ImageField(upload_to=get_image_name_by_slug, verbose_name='Изображение 1414x2000')

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
            self.slug = self.__class__.objects.first().slug
        else:  
            self.slug = get_uuid()    
        super().save(*args, **kwargs)
        with Image.open(self.image) as img:
            img = img.resize((1414, 2000))
            img.save(self.image.path)
        
    class Meta:
        verbose_name = 'Меню завтраков'
        verbose_name_plural = 'Меню завтраков'

class Menu(models.Model):
    slug = models.SlugField(max_length=36, verbose_name='Slug', blank=True, db_index=True) 
    page1 = models.ImageField(upload_to=get_image_name_by_slug, verbose_name='Страница 1 1414x2000')
    page2 = models.ImageField(upload_to=get_image_name_by_slug, verbose_name='Страница 2 1414x2000')

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
            self.slug = self.__class__.objects.first().slug
        else:  
            self.slug = get_uuid()    
        super().save(*args, **kwargs)
        for image in [self.page1, self.page2]:
            with Image.open(image) as img:
                img = img.resize((1414, 2000))
                img.save(image.path)
        
    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

class BarMenu(models.Model):
    slug = models.SlugField(max_length=36, verbose_name='Slug', blank=True, db_index=True) 
    page1 = models.ImageField(upload_to=get_image_name_by_slug, verbose_name='Страница 1 1414x2000')
    page2 = models.ImageField(upload_to=get_image_name_by_slug, verbose_name='Страница 2 1414x2000')

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
            self.slug = self.__class__.objects.first().slug
        else:  
            self.slug = get_uuid()    
        super().save(*args, **kwargs)
        for image in [self.page1, self.page2]:
            with Image.open(image) as img:
                img = img.resize((1414, 2000))
                img.save(image.path)
        
    class Meta:
        verbose_name = 'Барное меню'
        verbose_name_plural = 'Барное меню'
