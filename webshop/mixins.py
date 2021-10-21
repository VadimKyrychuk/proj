from django.views.generic.detail import SingleObjectMixin
from .models import Category
from django.views.generic import View
from .models import Basket, Customer

class CategoryMixin(SingleObjectMixin):
    def get_context_data(self, **kwargs):
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
        self.basket.save()
        return super().dispatch(request, *args, **kwargs)