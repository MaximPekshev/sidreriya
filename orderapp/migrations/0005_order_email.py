# Generated by Django 3.0.5 on 2020-06-24 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0004_order_cook_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.CharField(blank=True, max_length=30, verbose_name='Email'),
        ),
    ]