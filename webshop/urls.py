
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', MainView.as_view()),
    path('products/<str:ct_model>/<str:slug>/', ProductDetail.as_view(), name='product_details'),
    path('category/<str:slug>/', CategoryDetail.as_view(), name='category_details'),
    path('basket/',  BasketView.as_view(), name='basket'),
    path('add-to-basket/<str:ct_model>/<str:slug>/',  AddToBasket.as_view(), name='add_to_basket')
]
