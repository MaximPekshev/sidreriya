# Generated by Django 3.0.5 on 2020-05-14 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goodapp', '0038_good_gastronomy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='gastronomy',
            field=models.TextField(blank=True, default='', max_length=512, verbose_name='Гастрономия'),
        ),
    ]
