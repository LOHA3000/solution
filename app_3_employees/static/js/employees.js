let BX24 = parent.BX24;

let users;
let departments;
let calls;

BX24.callMethod(
    "user.get",
    {},
    function(result)
    {
        if(result.error())
            console.error(result.error());
        else {
            users = result.data();
            all_load();
        }
    }
);

BX24.callMethod(
    "department.get",
    {},
    function(result)
    {
        if(result.error())
            console.error(result.error());
        else {
            departments = result.data();
            all_load();
        }
    }
);

date = new Date();
date.setDate(date.getDate() - 1);

BX24.callMethod(
    "voximplant.statistic.get",
    {
        "FILTER": {">CALL_DURATION": 60,
                   ">CALL_START_DATE": date.toISOString(),
                   },
    },
    function(result)
    {
        if(result.error())
            console.error(result.error());
        else {
            calls = result.data();
            all_load();
        }
    }
);

function all_load() {
    if (users == undefined || departments == undefined || calls == undefined) {
        return;
    }

    let departments_map = {};
    let departments_weight = {};
    let users_map = {};
    let calls_map = {};
    departments.forEach(d => {
        departments_map[d.ID] = d;
        departments_weight[d.ID] = 1;
        if (d.PARENT)
            departments_weight[d.ID] += departments_weight[d.PARENT];
    });
    users.forEach(u => {
        users_map[u.ID] = u;
        calls_map[u.ID] = 0;
    });
    calls.forEach(c => calls_map[c.PORTAL_USER_ID] += 1);

    let table = document.querySelector('table');

    for (let user of users) {
        row = document.createElement('tr');
        table.appendChild(row);
        // фото
        user_info = document.createElement('td');
        if (user.PERSONAL_PHOTO) {
            image = document.createElement('img')
            image.src = user.PERSONAL_PHOTO;
            user_info.appendChild(image);
        }
        else
            user_info.innerHTML = 'без фото'
        user_info.setAttribute('rowspan', user.UF_DEPARTMENT.length);
        row.appendChild(user_info);
        // имя
        user_info = document.createElement('td');
        user_info.innerHTML = `${user.LAST_NAME} ${user.NAME}`;
        user_info.setAttribute('onclick', `open_user_in_slider(${user.ID});`);
        user_info.setAttribute('rowspan', user.UF_DEPARTMENT.length);
        user_info.classList.add('open-in-slider');
        row.appendChild(user_info);
        // отделы и руководитель
        let department_row = row;
        for (let department_id of user.UF_DEPARTMENT.sort((a, b) => departments_weight[b] - departments_weight[a])) {
            // название
            department_info = document.createElement('td');
            department_info.innerHTML = departments_map[department_id].NAME;
            if (user.ID == departments_map[department_id].UF_HEAD)
                department_info.innerHTML += ' (Руководитель)';
            department_row.appendChild(department_info);
            // руководитель
            department_info = document.createElement('td');
            if (departments_map[department_id].UF_HEAD && user.ID != departments_map[department_id].UF_HEAD) {
                department_head = users_map[departments_map[department_id].UF_HEAD];
                department_info.innerHTML = `${department_head.LAST_NAME} ${department_head.NAME}`;
                department_info.setAttribute('onclick', `open_user_in_slider(${department_head.ID});`);
                department_info.classList.add('open-in-slider');
            }
            department_row.appendChild(department_info);
            department_row = document.createElement('tr');
            table.appendChild(department_row);
        }
        // звонки
        user_info = document.createElement('td');
        user_info.innerHTML = calls_map[user.ID];
        user_info.setAttribute('rowspan', user.UF_DEPARTMENT.length);
        row.appendChild(user_info);
    }

    setTimeout(parent.resize_iframe_container, 500);
}

function open_user_in_slider(user_id) {
    BX24.init(
        function()
        {
            BX24.openPath(
                `/company/personal/user/${user_id}/`,
                function(result)
                {
                    console.log(result);
                }
            );
        }
    );
}

function create_new_call_form() {
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
    let form_content = fetch('/employees/create_call_form', {credentials: 'include'}).then(r => r.text())
    form_content.then(t => {
        form_container.innerHTML = t;
        form = form_container.querySelector('form');
        form.onsubmit = () => {
            let data = new FormData(form);
            response = fetch('/employees/create_call', {method: 'POST', body: data});
            modal.classList.remove('opened');
            setTimeout(() => {
                modal.remove();
                response.then(() => {window.location.reload();})
            }, 500)
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