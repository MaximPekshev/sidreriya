# Generated by Django 3.0.5 on 2020-06-10 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer',
            name='apartments',
            field=models.CharField(blank=True, max_length=10, verbose_name='Кв.'),
        ),
        migrations.AddField(
            model_name='buyer',
            name='house',
            field=models.CharField(blank=True, max_length=10, verbose_name='Дом'),
        ),
        migrations.AddField(
            model_name='buyer',
            name='locality',
            field=models.CharField(blank=True, max_length=20, verbose_name='Нас. пункт'),
        ),
        migrations.AddField(
            model_name='buyer',
            name='street',
            field=models.CharField(blank=True, max_length=30, verbose_name='Улица'),
        ),
    ]