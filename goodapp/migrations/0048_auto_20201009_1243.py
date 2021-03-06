# Generated by Django 3.1.2 on 2020-10-09 09:43

from django.db import migrations, models
import goodapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('goodapp', '0047_set_lunch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='set_lunch',
            name='date',
            field=models.DateField(unique=True),
        ),
        migrations.AlterField(
            model_name='set_lunch',
            name='image',
            field=models.ImageField(default=None, upload_to=goodapp.models.get_image_name_without_slug, verbose_name='Изображение'),
        ),
    ]
