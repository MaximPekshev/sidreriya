# Generated by Django 3.0.5 on 2020-06-08 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authapp', '0001_initial'),
        ('goodapp', '0040_auto_20200515_0725'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summ', models.DecimalField(blank=True, decimal_places=0, default=0, editable=False, max_digits=15, verbose_name='Сумма заказа')),
                ('order_number', models.CharField(max_length=10, verbose_name='Номер заказа')),
                ('address', models.CharField(blank=True, max_length=1024, verbose_name='Адрес')),
                ('buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authapp.Buyer')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='Order_Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=0, max_digits=15)),
                ('price', models.DecimalField(decimal_places=0, max_digits=15)),
                ('summ', models.DecimalField(decimal_places=0, max_digits=15)),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='goodapp.Good')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orderapp.Order')),
            ],
        ),
    ]
