import datetime


class StructDeal:
    def __init__(self, data, fields_params, manuals=None, join_fields=None, hide_fields=None):
        for key, value in data.items():
            if fields_params[key]['type'] == 'datetime':
                value = datetime.datetime.fromisoformat(value).strftime('%d.%m.%Y %H:%M:%S')
            elif fields_params[key]['type'] == 'date':
                value = datetime.datetime.fromisoformat(value).strftime('%d.%m.%Y')
            self.__setattr__(key, value)
        self.fields_params = fields_params
        self.headers = tuple(data.keys())
        self.manuals = dict() if manuals is None else manuals
        self.join_fields = dict() if join_fields is None else join_fields
        self.hide_fields = list() if hide_fields is None else hide_fields

    def __repr__(self):
        return f'<StructDeal ID={self.ID}>'

    @property
    def params(self):
        params = []
        for key in self.headers:
            if key in self.hide_fields:
                continue
            field = self.fields_params[key]['title']
            value = self.__getattribute__(key)
            if key in self.manuals:
                if value is None:
                    value = ''
                else:
                    value = self.manuals[key][value]
            if key in self.join_fields:
                add_values = []
                for add_key in self.join_fields[key]['fields']:
                    add_value = self.__getattribute__(add_key)
                    if add_key in self.manuals:
                        add_value = self.manuals[add_key][add_value]
                    add_values.append(add_value)
                value = self.join_fields[key]['method'](value, add_values)
            params.append((field, value))
        return params
