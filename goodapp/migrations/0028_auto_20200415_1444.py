# Generated by Django 3.0.5 on 2020-04-15 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goodapp', '0027_auto_20200415_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='category',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='goodapp.Category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='good',
            name='manufacturer',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='goodapp.Manufacturer', verbose_name='Производитель'),
        ),
    ]