# Generated by Django 3.0.5 on 2020-07-06 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart_item',
            name='quantity',
            field=models.DecimalField(decimal_places=1, max_digits=15),
        ),
    ]