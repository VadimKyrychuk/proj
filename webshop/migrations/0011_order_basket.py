# Generated by Django 3.2.8 on 2021-10-25 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0010_auto_20211023_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='basket',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webshop.basket', verbose_name='Корзина'),
        ),
    ]
