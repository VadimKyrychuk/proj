from django import template
from django.utils.safestring import mark_safe
from webshop.models import Smartphone

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
        'Бренд': 'brand',
        'Диагональ': 'diagonal',
        'Дисплей': 'display',
        'Процессор': 'cpu',
        'Оперативная память': 'ram',
        'Видеокарта': 'video'},

    'smartphone': {
        'Бренд': 'brand',
        'Модель смартфона': 'model_smart',
        'Диаональ': 'diagonal',
        'Разрешение экрана': 'resolution',
        'Объем аккумулятора': 'accum',
        'Оперативная память': 'ram',
        'Возможность использования SD': 'sd_card',
        'Максимальный объем SD': 'sd_card_max_size',
        'Главная камера': 'main_cam',
        'Фронтальная камера': 'front_cam',
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
<<<<<<< HEAD
    for name, value in PRODUCT_CHARACTERISTIC[model_name].items():
        print(value)
        if isinstance(product, Smartphone):
            table_content += TABLE_MAIN_CONTENT.format(name=name, value=getattr(product, value))
=======
    print(model_name)
    for name, value in PRODUCT_CHARACTERISTIC[model_name].items():
        table_content += TABLE_MAIN_CONTENT.format(name=name, value=getattr(product, value))
>>>>>>> 5e2533450e3c3d811c2029e05abd0614cb263735
    return table_content