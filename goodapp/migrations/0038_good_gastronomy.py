# Generated by Django 3.0.5 on 2020-05-14 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goodapp', '0037_auto_20200429_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='good',
            name='gastronomy',
            field=models.TextField(blank=True, default='', max_length=512, verbose_name='Гастронимия'),
        ),
    ]
