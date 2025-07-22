from integration_utils.bitrix24.models import BitrixUserToken
from main_page.localization import manuals


class Catalog:
    def __init__(self, info):
        self.name = info['name']
        self.id = info['iblockId']


class CatalogsCRM:
    def __init__(self):
        but = BitrixUserToken.objects.filter(user__is_admin=True).first()
        catalogs = but.call_list_method('catalog.catalog.list')['catalogs']
        self.head = None
        self.variations = None

        for catalog_data in catalogs:
            if not 'CRM' in catalog_data['name']:
                continue
            if not catalog_data['productIblockId'] is None: # вариации
                self.variations = Catalog(catalog_data)
            else:
                self.head = Catalog(catalog_data)

        assert not self.head is None
        assert not self.variations is None


catalogs_crm = CatalogsCRM()

PRODUCTS_AUTOCOMPLETE_FIELDS = ['id', 'iblockId', 'name']


def head_product_autocomplete(but, uid='', name=''):
    if not uid and not name:
        return []

    filter_ = {'iblockId': catalogs_crm.head.id}
    if uid:
        filter_['id'] = uid
    else:
        filter_['%name'] = name

    products = but.call_list_method('catalog.product.list',
                                    fields={'select': PRODUCTS_AUTOCOMPLETE_FIELDS, 'filter':filter_})['products']
    return products


def head_product_variations(but, uid):
    filter_ = {'iblockId': catalogs_crm.variations.id, 'parentId': uid}

    products = but.call_list_method('catalog.product.list',
                                    fields={'select': PRODUCTS_AUTOCOMPLETE_FIELDS, 'filter': filter_})['products']
    return products


class Product:
    def __init__(self, info, image_urls, type_):
        self.name = info['name']
        self.image_urls = image_urls
        if info['detailText']:
            self.description = info['detailText']
        if type_ == 'variation':
            measure = manuals['measure'][info['measure']]
            price = manuals['CURRENCY_ID'][info['currency']].replace('#', str(info['price']))
            self.price_str = lambda: f'{measure.lower()} за {price}'
        else:
            self.price_str = ''


def product_info(but, uid, type_):
    select = ['id', 'iblockId']
    if type_ == 'head':
        price = {}
        select += ['name', 'detailText']
        iblockId = catalogs_crm.head.id
    elif type_ == 'variation':
        price = but.call_list_method('catalog.price.list', fields={'filter': {'productId': uid},
                                                                   'select': ['price', 'currency']})['prices'][0]
        select += ['name', 'detailText', 'measure']
        iblockId = catalogs_crm.variations.id
    else:
        return {}
    info = but.call_list_method('catalog.product.list', fields={'filter': {'iblockId': iblockId, 'id': uid}, 'select': select})['products'][0]
    info.update(price)

    images = but.call_list_method('catalog.productImage.list', fields={'productId': uid})['productImages']
    image_urls = [e['detailUrl'] for e in images]
    return Product(info, image_urls, type_)
