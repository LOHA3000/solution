function import_contacts() {
    let form = document.querySelector('form[name="import"]');
    let data = new FormData(form);
    if (!data.get('file').name)
        return
    fetch('/contacts/import', {method: 'POST', body: data}).then(() => {
        alert('Импортирование завершено');
    });
}

function export_contacts() {
    let form = document.querySelector('form[name="export"]');
    let data = new FormData(form);
    response = fetch('/contacts/export', {method: 'POST', body: data});
    response.then(r => r.blob()).then(r => {
        let a = document.createElement('a');
        a.download = 'contacts.' + data.get('file_format');
        a.href = URL.createObjectURL(r);
        a.click();
        setTimeout(a.remove, 500);
    });
}

function changeAvailableImportFormats() {
    let file_format = document.querySelector('#import-file-format').value;
    let mimetype;
    switch (file_format) {
        case ('csv'):
            mimetype = 'text/csv'; break;
        case ('xlsx'):
            mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'; break;
    }
    let file_input = document.querySelector('form[name="import"] input[type=file]');
    file_input.accept = mimetype;
}