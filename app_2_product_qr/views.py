from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

from .services import head_product_autocomplete, head_product_variations, product_info
from b24apps.settings import DOMAIN
from integration_utils.bitrix24.models import BitrixUserToken
from .models import QR

import json
from uuid import uuid4
import qrcode
from io import BytesIO
from base64 import b64encode


@main_auth(on_cookies=True)
def main(request):
    return render(request, 'product_qr.html')


@main_auth(on_cookies=True)
def autocomplete(request):
    but = request.bitrix_user_token
    suggestions = head_product_autocomplete(but, request.GET.get('uid'), request.GET.get('name'))
    return HttpResponse(json.dumps(suggestions), content_type='application/json')


@main_auth(on_cookies=True)
def get_variations(request):
    but = request.bitrix_user_token
    variations = head_product_variations(but, request.GET.get('uid'))
    return HttpResponse(json.dumps(variations), content_type='application/json')


@main_auth(on_cookies=True)
def get_product_info(request):
    but = request.bitrix_user_token
    product = product_info(but, request.GET.get('uid'), request.GET.get('type'))
    return render(request, 'product.html', context={'product': product})


@main_auth(on_cookies=True)
def create_qr(request):
    if request.method == 'POST':
        print(request.POST)
        but = request.bitrix_user_token

        uuid = str(uuid4())
        qr_img = qrcode.make(f'https://{DOMAIN}/product_qr/show?token={uuid}', error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format='PNG')
        base64_qr = b64encode(qr_buffer.getvalue()).decode('utf-8')

        QR.objects.create(uuid=uuid, head_product=request.POST.get('head_uid'),
                          variation=request.POST.get('variation_uid'), base64=base64_qr)

        return HttpResponse('OK', 201)
    return HttpResponseForbidden


@main_auth(on_cookies=True)
def get_qr(request):
    images = QR.objects.filter(head_product=request.GET.get('head_product'), variation=request.GET.get('variation'))
    images = [img.base64 for img in images]
    return render(request, 'qr_gallery.html', context={'b64_images': images})


def show_by_qr(request):
    product = QR.objects.filter(uuid=request.GET.get('token')).first()
    if not product:
        return HttpResponseForbidden()
    but = BitrixUserToken.objects.filter(user__is_admin=True).first()
    return render(request, 'product_public_card.html',
                  context={'head_product': product_info(but, product.head_product, 'head'),
                           'variation': product_info(but, product.variation, 'variation')})