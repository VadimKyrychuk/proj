# Generated by Django 3.2.8 on 2021-11-06 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0012_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notebook',
            name='image_product',
            field=models.ImageField(upload_to='media/<django.db.models.fields.CharField>', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='smartphone',
            name='image_product',
            field=models.ImageField(upload_to='media/<django.db.models.fields.CharField>', verbose_name='Изображение'),
        ),
    ]