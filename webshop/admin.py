from django.contrib import admin
from .models import *
from django import forms


class NotebookCategoryChoice(forms.ModelChoiceField):
    pass

class SmartphonesCategoryChoice(forms.ModelChoiceField):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Notebook)
class NotebookAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return NotebookCategoryChoice(Category.objects.filter(slug_category='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Smartphone)
class SmartphoneAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return SmartphonesCategoryChoice(Category.objects.filter(slug_category='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    pass


@admin.register(BasketProduct)
class BasketProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass

