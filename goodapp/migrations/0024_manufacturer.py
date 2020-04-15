# Generated by Django 3.0.5 on 2020-04-15 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goodapp', '0023_auto_20200415_1314'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Наименование')),
                ('name_en', models.CharField(blank=True, max_length=150, verbose_name='Наименование на английском')),
                ('description', models.TextField(blank=True, max_length=1024, verbose_name='Описание')),
                ('meta_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='meta name')),
                ('meta_description', models.TextField(blank=True, max_length=1024, null=True, verbose_name='meta description')),
                ('slug', models.SlugField(blank=True, max_length=36, verbose_name='Url')),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goodapp.Good', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Производитель',
                'verbose_name_plural': 'Производители',
            },
        ),
    ]
