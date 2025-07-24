window.onload = load_active_tab;

function load_active_tab() {
    let active_tab = document.querySelector('input[name="tab"]:checked').getAttribute('id');
    const main_page = {
            deals: load_last_10_deals,
            ['product-qr']: product_qr,
            employees: employees_table,
            map: company_map,
            };
    main_page[active_tab]();
}

function reload_iframe_container(src) {
    let container = document.querySelector('.content-container');
    while (container.firstChild) { container.removeChild(container.firstChild); }

    const iframe = document.createElement("iframe");
    iframe.src = src;
    iframe.frameBorder = '0';
    iframe.scrolling = 'no';
    document.querySelector('.content-container').appendChild(iframe);

    iframe.onload = () => resize_iframe_container();
}

function resize_iframe_container() {
    iframe = document.querySelector('iframe');
    let innerDoc = iframe.contentDocument || iframe.contentWindow.document;
    innerDoc.body.style['min-width'] = 'max-content';
    innerDoc.body.style['min-height'] = 'max-content';
    innerDoc.body.style['margin'] = '0';
    innerDoc.body.style['padding-bottom'] = '42px';
    iframe.height = innerDoc.body.scrollHeight + 'px';
    iframe.width = innerDoc.body.scrollWidth + 'px';
}

function load_last_10_deals() {
    reload_iframe_container('/deals/')
}

function product_qr() {
    reload_iframe_container('/product_qr/')
}

function employees_table() {
    reload_iframe_container('/employees/')
}

function company_map() {
    reload_iframe_container('/map/')
}