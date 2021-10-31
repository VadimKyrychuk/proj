from django.urls import path, include
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', MainView.as_view(), name='base'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetail.as_view(), name='product_details'),
    path('category/<str:slug>/', CategoryDetail.as_view(), name='category_details'),
    path('basket/',  BasketView.as_view(), name='basket'),
    path('add-to-basket/<str:ct_model>/<str:slug>/',  AddToBasket.as_view(), name='add_to_basket'),
    path('remove-from-basket/<str:ct_model>/<str:slug>/',  DeleteFromBasket.as_view(), name='delete_from_basket'),
    path('change-quant/<str:ct_model>/<str:slug>/', ChangeQuant.as_view(), name='change_quant'),
    path('check/',  CheckView.as_view(), name='check'),
    path('make-order/',  MakeOrder.as_view(), name='make_order'),
    path('login/',  LoginView.as_view(), name='login'),
    path('logout/',  LogoutView.as_view(next_page='/'), name='logout'),
    path('registration/',  RegistrationView.as_view(), name='registration'),
    path('profile/',  Profile.as_view(), name='profile')
]
