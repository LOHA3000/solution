from django.urls import path
from .views import last_deals, create_deal_form, create_deal

urlpatterns = [
    path('', last_deals),
    path('create_deal_form', create_deal_form),
    path('create', create_deal),
]