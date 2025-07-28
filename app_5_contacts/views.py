from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, FileResponse

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from .services import check_companies_and_contacts, Parse

from copy import deepcopy


@main_auth(on_cookies=True)
def main(request):
    return render(request, 'contacts.html')


@main_auth(on_cookies=True)
def import_contacts(request):
    if request.method == 'POST':
        if request.FILES['file'].name.split('.')[-1] != request.POST.get('file_format'):
            return HttpResponseForbidden()
        but = request.bitrix_user_token
        print(request.POST)
        file_parse = Parse(request.FILES['file'])
        companies, contacts = check_companies_and_contacts(but)
        new_contacts, new_companies, contacts_updates = file_parse.differ(contacts, companies)

        change_query = []
        change_log = []

        for contact in new_contacts:
            change_query.append(('crm.contact.add', {'fields': {
                'NAME': contact['NAME'],
                'LAST_NAME': contact['LAST_NAME'],
                'PHONE': [{'VALUE': phone} for phone in contact['PHONE']],
                'EMAIL': [{'VALUE': phone} for phone in contact['EMAIL']],
            }}))
            change_log.append(('contact', contact))
        for company in new_companies:
            change_query.append(('crm.company.add', {'fields': {'TITLE': company}}))
            change_log.append(('company', company))
        for uid, updates in contacts_updates.items():
            update_with = {'id': uid, 'fields': {}}
            if 'PHONE' in updates:
                update_with['fields']['PHONE'] = [{'VALUE': phone} for phone in updates['PHONE']]
            if 'EMAIL' in updates:
                update_with['fields']['EMAIL'] = [{'VALUE': email} for email in updates['EMAIL']]
            change_query.append(('crm.contact.update',update_with))

        for result, (target, data) in zip(but.batch_api_call(change_query).values(), change_log):
            if target == 'contact':
                data_ = deepcopy(data)
                data_['COMPANY'].clear()
                contacts.add(result['result'], data_)
            elif target == 'company':
                companies.add(result['result'], data)

        change_query.clear()
        change_log.clear()
        new_contacts, new_companies, contacts_updates = file_parse.differ(contacts, companies)

        for uid, updates in contacts_updates.items():
            if 'COMPANY' in updates:
                for company in updates['COMPANY']:
                    company_id = companies.by_name(company)
                    change_query.append(('crm.contact.company.add',
                                         {'id': uid, 'fields': {'COMPANY_ID': company_id}}))

        but.batch_api_call(change_query)

        return HttpResponse('OK', status=201)
    return HttpResponseForbidden()


@main_auth(on_cookies=True)
def export_contacts(request):
    if request.method == 'POST':
        but = request.bitrix_user_token
        print(request.POST)
        companies, contacts = check_companies_and_contacts(but)

        if request.POST.get('file_format') == 'csv':
            file = contacts.as_csv()
            mimetype = 'text/csv'
        elif request.POST.get('file_format') == 'xlsx':
            file = contacts.as_xlsx()
            mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        else:
            return HttpResponseForbidden()
        return FileResponse(file, as_attachment=True, content_type=mimetype)
    return HttpResponseForbidden()