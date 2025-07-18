from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from .services import StructDeal
from main_page.localization import *
from .forms import NewDealForm

SELECT_DEAL_FIELDS = ['ID', 'TITLE', 'OPPORTUNITY', 'CURRENCY_ID', 'STAGE_ID',
                      'TYPE_ID', 'BEGINDATE', 'CLOSEDATE', 'DATE_CREATE', 'UF_CRM_1752748792590']
ALL_DEAL_FIELDS = ['*', 'UF_*']
HIDE_DEAL_FIELDS = ['ID', 'CURRENCY_ID']


@main_auth(on_cookies=True)
def last_deals(request):
    but = request.bitrix_user_token

    deals = but.call_list_method('crm.deal.list', fields={'select': SELECT_DEAL_FIELDS,
                                                          # 'select': ALL_DEAL_FIELDS,
                                                          'filter': {'CLOSED': 'N'},
                                                          'order': {'DATE_CREATE': 'DESC'}})[:10]
    # размер страницы ответа всегда 50 записей, поэтому происходит простой срез

    join_fields = {'OPPORTUNITY': {'fields': ['CURRENCY_ID'],
                                   'method': lambda value, to_add: to_add[0].replace('#', value)}}

    _all = [StructDeal(t, deal_fields, manuals, join_fields=join_fields, hide_fields=HIDE_DEAL_FIELDS) for t in deals]
    if len(_all):
        def get_localized(key):
            if key.startswith('UF_CRM_'):
                return 'formLabel'
            else:
                return 'title'

        table_headers = [deal_fields[key][get_localized(key)] for key in _all[0].headers if key not in HIDE_DEAL_FIELDS]
    else:
        table_headers = tuple()
    return render(request, 'deals.html',
                  {'list': enumerate(_all, start=1), 'headers': table_headers})


@main_auth(on_cookies=True)
def create_deal_form(request):
    form = NewDealForm()
    return render(request, 'deal_form.html', {'form': form})


@main_auth(on_cookies=True)
def create_deal(request):
    if request.method == 'POST':
        print(request.POST)
        but = request.bitrix_user_token
        new_id = but.call_list_method('crm.deal.add',
                                      fields={'fields': {
                                          'TITLE': request.POST.get('title'),
                                          'OPPORTUNITY': request.POST.get('opportunity'),
                                          'CURRENCY_ID': request.POST.get('currency'),
                                          'STAGE_ID': request.POST.get('stage'),
                                          'TYPE_ID': request.POST.get('_type'),
                                          'BEGINDATE': request.POST.get('begin_date'),
                                          'CLOSEDATE': request.POST.get('begin_date'),
                                          'UF_CRM_1752748792590': request.POST.get('payment_method')}})
        check = but.call_list_method('crm.deal.get', fields={'id': new_id})
        return HttpResponse('OK', 201)
    return HttpResponseForbidden