from django import forms


class NewCallForm(forms.Form):
    who = forms.ChoiceField(label='От кого')
    duration =  forms.IntegerField(label='Длительность (с)', min_value=1)

    def __init__(self, users):
        super().__init__()

        self.fields['who'] = forms.ChoiceField(
            label='От кого', choices=((u['ID'], f"{u['LAST_NAME']} {u['NAME']}") for u in users))