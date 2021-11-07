from django.contrib import admin
from .models import *
from django.forms import ModelChoiceField, ModelForm, ValidationError
from modeltranslation.admin import TranslationAdmin

class SmartphoneAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and not instance.sd_card:
            self.fields['sd_card_max_size'].widget.attrs.update({
                'readonly':True, 'style': 'backgrond : #121212'
            })

    def clean(self):
        if not self.cleaned_data['sd_card']:
            self.cleaned_data['sd_card_max_size'] = None
        return self.cleaned_data


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    pass


@admin.register(Notebook)
class NotebookAdmin(TranslationAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Smartphone)
class SmartphoneAdmin(TranslationAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    change_form_template = 'admin.html'
    form = SmartphoneAdminForm


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    pass


@admin.register(BasketProduct)
class BasketProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


