
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index),
    path('products/<str:ct_model>/<str:slug>/', ProductDetail.as_view(), name='product_details'),
    path('category/<str:slug>/', CategoryDetail.as_view(), name='category_details')
]
