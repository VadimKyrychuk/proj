from django.views.generic.detail import SingleObjectMixin
from .models import Category
from django.views.generic import View
from .models import Basket, Customer, Notebook, Smartphone

class CategoryMixin(SingleObjectMixin):

    CATEGORY_SLUG = {
        'notebooks': Notebook,
        'smartphones': Smartphone
    }

    def get_context_data(self, **kwargs):
        if isinstance(self.get_object(), Category):
            model = self.CATEGORY_SLUG[self.get_object().slug]
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.get_category_for_navbar()
            context['category_prod'] = model.objects.all()
            return context
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.get_category_for_navbar()
        return context


class CartMix(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(user=request.user)
            basket = Basket.objects.filter(holder=customer, in_order=False).first()
            if not basket:
                basket = Basket.objects.create(holder=customer)
        else:
            basket = Basket.objects.filter(anonym_user=True).first()
            if not basket:
                basket = Basket.objects.create(anonym_user = True)
        self.basket = basket
        return super().dispatch(request, *args, **kwargs)