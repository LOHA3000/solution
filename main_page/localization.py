from integration_utils.bitrix24.models import BitrixUserToken
import html


but = BitrixUserToken.objects.filter(user__is_admin=True).first()
deal_fields = but.call_list_method('crm.deal.fields')
stage_types = but.call_list_method('crm.status.entity.items', fields={'entityId': 'DEAL_STAGE'})
deal_types = but.call_list_method('crm.status.entity.items', fields={'entityId': 'DEAL_TYPE'})
currency_types = but.call_list_method('crm.currency.list')
measure_type = but.call_list_method('catalog.measure.list')['measures']

manuals = {
    'STAGE_ID': {e['STATUS_ID']: e['NAME'] for e in stage_types},
    'CURRENCY_ID': {e['CURRENCY']: html.unescape(e['FORMAT_STRING']) for e in currency_types},
    'TYPE_ID': {e['STATUS_ID']: e['NAME'] for e in deal_types},
    'UF_CRM_1752748792590': {e['ID']: e['VALUE'] for e in deal_fields['UF_CRM_1752748792590']['items']},
    'measure': {e['id']: e['measureTitle'] for e in measure_type},
}
del but