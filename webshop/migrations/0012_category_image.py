# Generated by Django 3.2.8 on 2021-11-02 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0011_order_basket'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='media/not.jpg', upload_to='', verbose_name='Изображение категории'),
        ),
    ]
