# Generated by Django 3.2.8 on 2021-10-17 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0002_notebook_smartphone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='slug_category',
            new_name='slug',
        ),
        migrations.RenameField(
            model_name='notebook',
            old_name='slug_product',
            new_name='slug',
        ),
        migrations.RenameField(
            model_name='smartphone',
            old_name='slug_product',
            new_name='slug',
        ),
    ]
