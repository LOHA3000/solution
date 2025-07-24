let BX24 = parent.BX24;

let domain = BX24.getDomain();
let company_type_id;
let requisite_type_id;

let requisites;
let companies;

let map;
initMap();

function startMarkerDrawing() {
    BX24.callMethod(
        "crm.enum.ownertype",
        {},
        function(result) {
            if (result.error())
                console.error(result.error());
            else {
                result.data().forEach(owner => {
                    if (owner.SYMBOL_CODE == 'COMPANY')
                        company_type_id = owner.ID;
                    else if (owner.SYMBOL_CODE == 'REQUISITE')
                        requisite_type_id = owner.ID;
                });
                collect_companies();
            }
        }
    );
}

function collect_companies() {
    BX24.callMethod(
        "crm.requisite.list",
        {
            select: ["ID", "ENTITY_ID"],
            filter: {ENTITY_TYPE_ID: company_type_id}
        },
        function(result)
        {
            if(result.error())
                console.error(result.error());
            else
            {
                requisites = {};
                result.data().forEach(r => requisites[r.ID] = r.ENTITY_ID);
                next_step();
            }
        }
    );

    BX24.callMethod(
        "crm.company.list",
        {
            select: ["TITLE", "LOGO", "ID"],
        },
        function(result)
        {
            if(result.error())
                console.error(result.error());
            else
            {
                companies = {};
                result.data().forEach(c => {
                    companies[c.ID] = c;
                    companies[c.ID].LOGO = `https://${domain}${c.LOGO.downloadUrl}`;
                });
                next_step();
            }
        }
    );

    function next_step() {
        if (!requisites || !companies)
            return;
        else
            collect_addresses();
    }
}

function collect_addresses() {
    BX24.callMethod(
        "crm.address.list",
        {
            select: ["*"],
            filter: {ENTITY_TYPE_ID: requisite_type_id}
        },
        function(result)
        {
            if(result.error())
                console.error(result.error());
            else
            {
                result.data().forEach(addr => {
                    geoCode(addr).then(r => r.json()).then(r => {
                        let point = r.response.GeoObjectCollection.featureMember[0].GeoObject.Point.pos;
                        companies[requisites[addr.ENTITY_ID]].GEO_POINT = point.split(' ').map(parseFloat);
                        add_new_marker(companies[requisites[addr.ENTITY_ID]])
                    });
                });
            }
        }
    );
}

function geoCode(address) {
    let params = new URLSearchParams({
        apikey: '3ca76f5c-95f9-4914-884d-89390043091d',
        geocode: `${address.CITY}, ${address.ADDRESS_1}`,
        lang: 'ru_RU',
        format: 'json',
    });
    return fetch(`https://geocode-maps.yandex.ru/v1/?${params.toString()}`)
}

async function initMap() {
    ymaps3.import.registerCdn('https://cdn.jsdelivr.net/npm/{package}', [
      '@yandex/ymaps3-default-ui-theme@0.0.19'
    ]);

    await ymaps3.ready;
    const {YMap, YMapDefaultSchemeLayer, YMapDefaultFeaturesLayer, YMapControls, YMapScaleControl, YMapMarker} = ymaps3;
    const {YMapZoomControl} = await ymaps3.import('@yandex/ymaps3-default-ui-theme');

    map = new YMap(
        document.getElementById('map'),
        {
            location: {
                center: [30.314997, 59.938784],
                zoom: 10
            },
            //showScaleInCopyrights: true // You can display the map scale as part of copyrights
        },
        [new YMapDefaultSchemeLayer({}), new YMapDefaultFeaturesLayer({})]
    );

    // Or place the scale of the map as a control anywhere on the map
    map.addChild(
        new YMapControls(
            {position: 'bottom left'},
            [new YMapScaleControl({})]
    ));
    map.addChild(
        new YMapControls(
            {position: 'right'},
            [new YMapZoomControl({})]
    ));

    startMarkerDrawing();
}

function add_new_marker(company) {
    const {YMapMarker} = ymaps3;

    console.log(company);

    const markerElement = document.createElement('div');
    let image = document.createElement('img');
    image.src = company.LOGO;
    markerElement.appendChild(image);
    let name = document.createElement('div');
    name.innerText = company.TITLE;
    markerElement.appendChild(name);
    markerElement.className = 'marker-class';

    map.addChild(
        new YMapMarker(
          {
            coordinates: company.GEO_POINT,
          },
          markerElement
    ));
}