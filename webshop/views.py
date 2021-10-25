from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.views.generic import DetailView, View
from .models import Notebook, Smartphone, Category, Latest, Customer, Basket, BasketProduct
from .mixins import CategoryMixin, CartMix
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import OrderForm
from .util import calculated_basket
from django.db import transaction


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
        context['basket'] = self.basket
        return context


class CategoryDetail(CartMix,CategoryMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basket'] = self.basket
        return context


class AddToBasket(CartMix, View):

    def get(self, request, *args, **kwargs):
        ct_model, prod_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=prod_slug)
        basket_product, created = BasketProduct.objects.get_or_create(
            user=self.basket.holder, basket=self.basket, content=content_type, object_id=product.id)
        if created:
            self.basket.products.add(basket_product)
        calculated_basket(self.basket)
        messages.add_message(request, messages.INFO, 'Товар успешно добавлен')
        return HttpResponseRedirect('/basket/')


class DeleteFromBasket(CartMix, View):
    def get(self, request, *args, **kwargs):
        ct_model, prod_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=prod_slug)
        basket_product = BasketProduct.objects.get(
            user=self.basket.holder, basket=self.basket, content=content_type,
            object_id=product.id
        )

        self.basket.products.remove(basket_product)
        basket_product.delete()
        calculated_basket(self.basket)
        messages.add_message(request, messages.INFO, 'Товар успешно удален')
        return HttpResponseRedirect('/basket/')

class BasketView(CartMix, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_category_for_navbar()
        content = {
            'basket': self.basket,
            'categories': categories
        }
        return render(request, 'basket.html', content)


class ChangeQuant(CartMix, View):

    def post(self, request, *args, **kwargs):
        ct_model, prod_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=prod_slug)
        basket_product = BasketProduct.objects.get(
            user=self.basket.holder, basket=self.basket, content=content_type,
            object_id=product.id
        )
        quant = int(request.POST.get('quant'))
        basket_product.quantity = quant
        basket_product.save()
        calculated_basket(self.basket)
        messages.add_message(request, messages.INFO, 'Количество изменено')
        return HttpResponseRedirect('/basket/')

class CheckView(CartMix, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_category_for_navbar()
        form = OrderForm(request.POST or None)
        content = {
            'basket': self.basket,
            'categories': categories,
            'form': form
        }
        return render(request, 'check.html', content)

class MakeOrder(CartMix, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.adress = form.cleaned_data['adress']
            new_order.buy_type = form.cleaned_data['buy_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.basket.in_order = True
            self.basket.save()
            new_order.basket = self.basket
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Спасибо за заказ, ближайшим временем наш менеджер свяжется с Вами')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/check/')

