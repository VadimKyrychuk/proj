from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.views.generic import DetailView, View
from .models import Notebook, Smartphone, Category, Latest, Customer, Basket, BasketProduct
from .mixins import CategoryMixin, CartMix
from django.http import HttpResponseRedirect


# def index(request):
#     category_for_navbar = Category.objects.get_category_for_navbar()
#     return render(request, 'base.html', {'categories':category_for_navbar})

class MainView(CartMix, View):

    def get(self, request, *args, **kwargs):

        category_for_navbar = Category.objects.get_category_for_navbar()
        products = Latest.objects.get_product_models('notebook', 'smartphone')
        content = {
            'categories': category_for_navbar,
            'products': products,
            'basket': self.basket
        }
        return render(request, 'base.html', content)


class ProductDetail(CartMix, CategoryMixin, DetailView):
    CT_MODEL_MODEL_CLASS = {
        'notebook': Notebook,
        'smartphone': Smartphone
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'product.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        return context

class CategoryDetail(CategoryMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'


class AddToBasket(CartMix, View):

    def get(self, request, *args, **kwargs):
        ct_model, prod_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=prod_slug)
        basket_product, created = BasketProduct.objects.get_or_create(
            user=self.basket.holder, basket=self.basket, content=content_type, object_id=product.id)
        if created:
            self.basket.products.add(basket_product)
        self.basket.save()
        return HttpResponseRedirect('/basket/')



class BasketView(CartMix, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_category_for_navbar()
        content = {
            'basket': self.basket,
            'categories': categories
        }
        return render(request, 'basket.html', content)
