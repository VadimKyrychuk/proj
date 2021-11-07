from modeltranslation.translator import register, TranslationOptions
from .models import Category, Notebook, Smartphone


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name_category',)


@register(Notebook)
class NotebookTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(Smartphone)
class SmartphoneTranslationOptions(TranslationOptions):
    fields = ('description',)

