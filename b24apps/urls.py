"""
URL configuration for b24apps project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main_page.views import start

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', start),
    path('deals/', include('app_1_deals_management.urls')),
    path('product_qr/', include('app_2_product_qr.urls')),
    path('employees/', include('app_3_employees.urls')),
    path('map/', include('app_4_company_map.urls')),
]
