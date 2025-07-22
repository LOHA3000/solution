let head_product;
let variation;
let exists = false;

function autocomplete_id() {
    let field_id = document.querySelector('input[name="id"]');
    let field_name = document.querySelector('input[name="title"]')
    clear_tips();

    field_name.value = '';
    field_name.placeholder = '—';

    const params = new URLSearchParams({ uid: field_id.value, name: '' }).toString();
    let response = fetch(`/product_qr/autocomplete?${params}`)
    response.then(r => r.json().then(r => r.forEach((s) => {
        field_name.placeholder = s['name'];
        load_suggestions(s['id'], s['name']);
    })));
}

function autocomplete_title() {
    let field_id = document.querySelector('input[name="id"]');
    let field_name = document.querySelector('input[name="title"]');
    clear_tips();

    let founded = load_suggestions('', field_name.value);
    field_id.value = '';
    field_name.placeholder = '';
    founded.then(f => { field_id.placeholder = (f.length == 0) ? '' : f.join('/'); });
}

function load_suggestions(uid, name) {
    let datalist = document.querySelector('datalist');

    const params = new URLSearchParams({ uid: '', name: name }).toString();
    response = fetch(`/product_qr/autocomplete?${params}`)

    let found = [];

    return response.then(r => r.json().then(r => r.forEach((s) => {
        let item_auto = document.createElement('option');
        item_auto.textContent = s['name'];
        datalist.appendChild(item_auto);
        if ((uid == '' && found.length == 0 && name == s['name']) || (uid != '' && uid == s['id'])) {
            load_variations(s['id']);
            head_product = s['id'];
            load_product_info(head_product, 'head')
        }
        if (name == s['name']) {
            found.push(s['id']);
        }
    }))).then(() => found);
}

function load_variations(uid) {
    let variation_selector = document.querySelector('select[name="variation"]');

    let variations_response = fetch(`/product_qr/variations?${new URLSearchParams({uid: uid}).toString()}`)
    variations_response.then(r => r.json().then(r => {
        r.forEach(s => {
            let item_auto = document.createElement('option');
            item_auto.textContent = s['name'];
            item_auto.value = s['id'];
            variation_selector.appendChild(item_auto);
        });
        variation_selector.selectedIndex = 0;
        select_variation();
    }));
}

function clear_tips() {
    let datalist = document.querySelector('datalist');
    while (datalist.firstChild) { datalist.removeChild(datalist.firstChild); }
    let variation_selector = document.querySelector('select[name="variation"]');
    while (variation_selector.firstChild) { variation_selector.removeChild(variation_selector.firstChild); }
    exists = false;
    document.querySelector('.head-product').innerHTML = '';
    document.querySelector('.product-variation').innerHTML = '';
    window.parent.resize_iframe_container();
}

function select_variation() {
    let variation_selector = document.querySelector('select[name="variation"]');
    variation = variation_selector.value;
    console.log(head_product, variation);
    exists = true;
    load_product_info(variation, 'variation');
    reload_created_qr();
}

function load_product_info(uid, type) {
    let info_response = fetch(`/product_qr/product_info?` +
        `${new URLSearchParams({uid: uid, type: type}).toString()}`)
    let container;
    if (type == 'head') {
        container = document.querySelector('.head-product')
    }
    else if (type == 'variation') {
        container = document.querySelector('.product-variation')
    }
    info_response.then(r => r.text()).then(r => {
        container.innerHTML = r
        setTimeout(window.parent.resize_iframe_container, 500);
    });
}

function create_qr() {
    let data = new FormData()
    data.append('head_uid', head_product);
    data.append('variation_uid', variation);
    fetch('/product_qr/create_qr', {method: 'POST', body: data}).then(reload_created_qr);
}

function reload_created_qr() {
    let container = document.querySelector('.created-qr')
    qr_response = fetch(`/product_qr/created_qr?` +
        `${new URLSearchParams({head_product: head_product, variation: variation}).toString()}`)
    qr_response.then(r => r.text()).then(r => {
        container.innerHTML = r;
        setTimeout(window.parent.resize_iframe_container, 500);
    });
}