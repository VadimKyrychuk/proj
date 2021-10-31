from django.db import models

def calculated_basket(basket):
    basket_data = basket.products.aggregate(models.Sum('total_price'), models.Count('id'))
    if basket_data.get('total_price__sum'):
        basket.total_price = basket_data.get('total_price__sum')
    else:
        basket.total_price = 0
    basket.total_products = basket_data['id__count']
    basket.save()