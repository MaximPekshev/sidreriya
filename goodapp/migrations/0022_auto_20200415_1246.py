# Generated by Django 3.0.5 on 2020-04-15 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goodapp', '0021_auto_20200415_1245'),
    ]

    operations = [
        migrations.RenameField(
            model_name='good',
            old_name='is_creator',
            new_name='is_manufacturer',
        ),
    ]
