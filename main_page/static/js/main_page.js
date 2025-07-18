window.onload = load_last_10_deals;

function reload_iframe_container(src) {
    document.querySelector('.content-container').innerHtml = '';

    const iframe = document.createElement("iframe");
    iframe.src = src;
    iframe.frameBorder = '0';
    iframe.scrolling = 'no';
    document.querySelector('.content-container').appendChild(iframe);

    iframe.onload = () => {
        let innerDoc = iframe.contentDocument || iframe.contentWindow.document;
        innerDoc.body.style['min-width'] = 'max-content';
        innerDoc.body.style['margin'] = '0';
        innerDoc.body.style['padding-bottom'] = '42px';
        innerDoc.body.style['min-height'] = 'max-content';
        iframe.height = innerDoc.body.scrollHeight + 'px';
        iframe.width = innerDoc.body.scrollWidth + 'px';
    }
}

function load_last_10_deals() {
    reload_iframe_container('/deals/')
}