from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_start=True, set_cookie=True)
def start(request):
    user = request.bitrix_user
    return render(request, 'index.html', {'user': user})
