function create_new_deal_form() {
    let modal = document.createElement('div');
    modal.classList.add('modal');
    let modal_content = document.createElement('div');
    modal.appendChild(modal_content);
    modal_content.classList.add('modal-content');

    let close_button = document.createElement('div');
    modal_content.appendChild(close_button);
    close_button.classList.add('close-btn');
    close_button.innerHTML = '<div class="leftright"></div><div class="rightleft"></div>';
    close_button.onclick = () => {
        modal.classList.remove('opened');
        setTimeout(() => {modal.remove()}, 500);
    };

    let form_container = document.createElement('div');
    let form_content = fetch('/deals/create_deal_form', {credentials: 'include'}).then(r => r.text())
    form_content.then(t => {
        form_container.innerHTML = t;
        form = form_container.querySelector('form');
        form.onsubmit = () => {
            let data = new FormData(form);
            response = fetch('/deals/create', {method: 'POST', body: data});
            modal.classList.remove('opened');
            setTimeout(() => {modal.remove()}, 500)
            response.then(() => {window.location.reload();})
            return false;
        }
    });
    modal_content.appendChild(form_container);

    to = window.parent.document || document;
    to.body.appendChild(modal);

    setTimeout(() => {
        modal.classList.add('opened');
    }, 50);
}
