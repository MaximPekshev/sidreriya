# Generated by Django 3.0.5 on 2020-04-15 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goodapp', '0029_auto_20200415_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturer',
            name='description',
            field=models.TextField(blank=True, max_length=2048, verbose_name='Описание'),
        ),
    ]
