from django.shortcuts import render
from django.views.generic import DetailView
from .models import Notebook, Smartphone, Category

def index(request):
    category_for_navbar = Category.objects.get_category_for_navbar()
    return render(request, 'base.html', {'categories':category_for_navbar})

class ProductDetail(DetailView):

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


class CategoryDetail(DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'