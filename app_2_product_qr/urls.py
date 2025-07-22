from django.urls import path
from .views import main, autocomplete, get_variations, get_product_info, create_qr, get_qr, show_by_qr

urlpatterns = [
    path('', main),
    path('autocomplete', autocomplete),
    path('variations', get_variations),
    path('product_info', get_product_info),
    path('create_qr', create_qr),
    path('created_qr', get_qr),
    path('show', show_by_qr),
]