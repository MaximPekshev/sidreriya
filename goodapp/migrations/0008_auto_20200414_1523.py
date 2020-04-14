# Generated by Django 3.0.5 on 2020-04-14 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goodapp', '0007_auto_20200414_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object_property_values',
            name='_property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goodapp.Properties', unique=True, verbose_name='Свойство'),
        ),
        migrations.AlterField(
            model_name='object_property_values',
            name='property_value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goodapp.Property_value', verbose_name='Значение'),
        ),
    ]
