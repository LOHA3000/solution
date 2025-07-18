from django import forms
from main_page.localization import *


class DateInput(forms.DateInput):
    input_type = 'date'


class NewDealForm(forms.Form):
    title = forms.CharField(label=deal_fields['TITLE']['title'])
    opportunity = forms.FloatField(label=deal_fields['OPPORTUNITY']['title'])
    currency = forms.ChoiceField(label=deal_fields['CURRENCY_ID']['title'],
                                 choices=((e['CURRENCY'], e['FULL_NAME']) for e in currency_types))
    stage =  forms.ChoiceField(label=deal_fields['STAGE_ID']['title'],
                               choices=((e['STATUS_ID'], e['NAME']) for e in stage_types))
    _type = forms.ChoiceField(label=deal_fields['TYPE_ID']['title'],
                              choices=((e['STATUS_ID'], e['NAME']) for e in deal_types))
    begin_date = forms.DateField(label=deal_fields['BEGINDATE']['title'], widget=DateInput)
    close_date = forms.DateField(label=deal_fields['CLOSEDATE']['title'], widget=DateInput)
    payment_method = forms.ChoiceField(label=deal_fields['UF_CRM_1752748792590']['formLabel'],
                                       choices=manuals['UF_CRM_1752748792590'].items())