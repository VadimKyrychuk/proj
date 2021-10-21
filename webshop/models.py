from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


current_user = get_user_model()


def get_count_model(*model_names):
    return [models.Count(model_name) for model_name in model_names]


class LatestManager:
    @staticmethod
    def get_product_models(*args, **kwargs):
        products = []
        cnt_models = ContentType.objects.filter(model__in=args)
        for cnt_model in cnt_models:
            model_prod = cnt_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_prod)
        return products


class Latest:
    objects = LatestManager()


class ManagerCategory(models.Manager):
    CATEGORY_COUNT_NAME = {
        'Ноутбуки': "notebook__count",
        "Смартфоны": "smartphone__count"
    }

    def get_query_set(self):
        return super().get_queryset()

    def get_category_for_navbar(self):
        count_model = get_count_model('notebook', 'smartphone')
        query_set = list(self.get_query_set().annotate(*count_model))
        info = [
            dict(name=c.name_category, url=c.get_absolute_url(),
                 count=getattr(c, self.CATEGORY_COUNT_NAME[c.name_category])) for c in query_set
        ]
        return info


class Category(models.Model):
    name_category = models.CharField(max_length=255, verbose_name='Название катеории')
    slug = models.SlugField(unique=True)
    objects = ManagerCategory()

    def __str__(self):
        return self.name_category

    def get_absolute_url(self):
        return reverse('category_details', kwargs={'slug': self.slug})


class Product(models.Model):
    class Meta:
        abstract = True  #

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    name_product = models.CharField(max_length=255, verbose_name='Название товара')
    slug = models.SlugField(unique=True)
    image_product = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return f'{self.category} {self.name_product} {self.price}'


class Notebook(Product):
    brand = models.CharField(max_length=255, verbose_name='Бренд ноутбука')
    diagonal = models.CharField(max_length=255, verbose_name="Диагональ")
    display = models.CharField(max_length=255, verbose_name="Тип дисплея")
    cpu = models.CharField(max_length=255, verbose_name="Процессор")
    ram = models.CharField(max_length=255, verbose_name="Оперативная память")
    video = models.CharField(max_length=255, verbose_name="Видеокарта")


    def __str__(self):
        return f'{self.category.name_category}: {self.name_product}'

    def get_absolute_url(self):
        return get_product_url(self, 'product_details')


class Smartphone(Product):
    brand = models.CharField(max_length=64, verbose_name='Бренд смартфона')
    model_smart = models.CharField(max_length=64, verbose_name='Модель смартфона')
    diagonal = models.CharField(max_length=255, verbose_name="Диагональ")
    display = models.CharField(max_length=255, verbose_name="Тип дисплея")
    resolution = models.CharField(max_length=255, verbose_name='Разрешение экрана')
    accum = models.CharField(max_length=255, verbose_name="Объем аккумулятора")
    ram = models.CharField(max_length=64, verbose_name="Оперативная память")
    sd_card = models.BooleanField(default=True, verbose_name="Возможность использования SD карты")
    sd_card_max_size = models.CharField(max_length=255, null=True, blank=True, verbose_name="Максимальный объем SD")
    main_cam = models.CharField(max_length=64, verbose_name="Главная камера")
    front_cam = models.CharField(max_length=64, verbose_name="Фронтальная камера")

    def __str__(self):
        return f'{self.category.name_category}: {self.name_product}'

    def get_absolute_url(self):
        return get_product_url(self, 'product_details')


class BasketProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    basket = models.ForeignKey('Basket', verbose_name='Корзина', on_delete=models.CASCADE,
                               related_name='related_basket')
    content = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    cont_object = GenericForeignKey('content', 'object_id')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Общая сумма')

    def __str__(self):
        return f'Товар: {self.cont_object.name_product} {self.cont_object.price}'

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.cont_object.price
        super().save(*args, **kwargs)


class Basket(models.Model):

    holder = models.ForeignKey('Customer', null=True ,on_delete=models.CASCADE, verbose_name='Пользователь')
    products = models.ManyToManyField(BasketProduct, blank=True, related_name='related_basket')
    total_products = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=12, default=0, decimal_places=2, verbose_name='Общая сумма')
    in_order = models.BooleanField(default=False)
    anonym_user = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id} {self.products}'

    def save(self, *args, **kwargs):
        basket_data = self.products.aggregate(models.Sum('total_price'), models.Count('id'))
        if basket_data.get('total_price__sum'):
            self.final_amount = basket_data.get('total_price__sum')
        else:
            self.final_amount = 0
        self.total_products = basket_data['id__count']
        super().save(*args, **kwargs)

class Customer(models.Model):
    user = models.ForeignKey(current_user, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    adress = models.CharField(max_length=255, verbose_name='Адресс проживания', null=True, blank=True)

    def __str__(self):
        return f'Пользователь: {self.user.first_name} {self.user.last_name}'
