# Generated by Django 3.0.5 on 2020-06-24 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0003_auto_20200610_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cook_time',
            field=models.CharField(blank=True, max_length=20, verbose_name='Время приготовления'),
        ),
    ]