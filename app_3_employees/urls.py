from django.urls import path
from .views import main, create_call_form, create_call

urlpatterns = [
    path('', main),
    path('create_call_form', create_call_form),
    path('create_call', create_call),
]