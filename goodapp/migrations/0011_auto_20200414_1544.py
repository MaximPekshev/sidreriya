# Generated by Django 3.0.5 on 2020-04-14 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goodapp', '0010_auto_20200414_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object_property_values',
            name='property_value',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='goodapp.Property_value', verbose_name='Значение'),
        ),
    ]
