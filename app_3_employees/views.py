import time

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from .forms import NewCallForm


@main_auth(on_cookies=True)
def main(request):
    return render(request, 'employees.html')


@main_auth(on_cookies=True)
def create_call_form(request):
    but = request.bitrix_user_token
    users = but.call_list_method('user.get')
    form = NewCallForm(users)
    return render(request, 'call_form.html', {'form': form})


@main_auth(on_cookies=True)
def create_call(request):
    if request.method == 'POST':
        print(request.POST)
        but = request.bitrix_user_token
        new_call = but.call_api_method('telephony.externalcall.register',
                                        params={'USER_ID': request.POST.get('who'),
                                                'PHONE_NUMBER': f'+7{str(time.time_ns())[-10:]}',
                                                'TYPE': 1, # исходящий
                                                'SHOW': 0, # скрыть карточку вызова
                                                })
        new_call_id = new_call['result']['CALL_ID']
        finish_call = but.call_api_method('telephony.externalcall.finish',
                                          params={'USER_ID': request.POST.get('who'),
                                                  'CALL_ID': new_call_id,
                                                  'DURATION': request.POST.get('duration')
                                                  })
        return HttpResponse('OK', 201)
    return HttpResponseForbidden