from django import template
from django.utils.safestring import mark_safe
from webshop.models import Smartphone
from django.utils.translation import ugettext_lazy as _

register = template.Library()

TABLE_HEAD = """
            <table class="table">
              <tbody>
            """

TABLE_BOTTOM = """
              </tbody>
            </table>
                """

TABLE_MAIN_CONTENT = """
             <tr>
                  <td>{name} </td>
                  <td>{value}</td>
                </tr>
                    """

PRODUCT_CHARACTERISTIC = {
    'notebook': {
        _('Бренд'): 'brand',
        _('Диагональ'): 'diagonal',
        _('Дисплей'): 'display',
        _('Процессор'): 'cpu',
        _('Оперативная память'): 'ram',
        _('Видеокарта'): 'video'},

    'smartphone': {
        _('Бренд'): 'brand',
        _('Модель смартфона'): 'model_smart',
        _('Диагональ'): 'diagonal',
        _('Разрешение экрана'): 'resolution',
        _('Объем аккумулятора'): 'accum',
        _('Оперативная память'): 'ram',
        _('Возможность использования SD'): 'sd_card',
        _('Максимальный объем SD'): 'sd_card_max_size',
        _('Главная камера'): 'main_cam',
        _('Фронтальная камера'): 'front_cam',
    }
}


@register.filter
def product_characteristic(product):
    model_name = product.__class__._meta.model_name
    if isinstance(product, Smartphone):
        if not product.sd_card:
            PRODUCT_CHARACTERISTIC['smartphone'].pop('Максимальный объем SD', None)
        else:
            PRODUCT_CHARACTERISTIC['smartphone']['Максимальный объем SD'] = 'sd_card_max_size'
    return mark_safe(TABLE_HEAD + get_prod_characteristic(product, model_name) + TABLE_BOTTOM)



def get_prod_characteristic(product, model_name):
    table_content = ''
    for name, value in PRODUCT_CHARACTERISTIC[model_name].items():
            table_content += TABLE_MAIN_CONTENT.format(name=name, value=getattr(product, value))
    print(table_content)
    return table_content
