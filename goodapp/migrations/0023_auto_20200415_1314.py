# Generated by Django 3.0.5 on 2020-04-15 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goodapp', '0022_auto_20200415_1246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='good',
            name='is_manufacturer',
        ),
        migrations.RemoveField(
            model_name='good',
            name='manufacturer',
        ),
    ]