from django.urls import path
from .views import main, import_contacts, export_contacts

urlpatterns = [
    path('', main),
    path('import', import_contacts),
    path('export', export_contacts),
]