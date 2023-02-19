
import requests
import xmltodict


key = "1VQDHXQ8EF73QTHESPT7UHU9AJQPLXXL"
ENDPOINT = "http://164.92.218.36:8080/api"


def test_can_get_api():
    response = requests.get(ENDPOINT, auth=(key, ""))
    assert response.status_code == 200


def test_can_get_address():
    response = requests.get(ENDPOINT + '/addresses', auth=(key, ""))
    assert response.status_code == 200


def create_xml_body():
    return """
    <prestashop
        xmlns:xlink="http://www.w3.org/1999/xlink">
        <address>
            <id_customer></id_customer>
            <id_manufacturer></id_manufacturer>
            <id_supplier></id_supplier>
            <id_warehouse></id_warehouse>
            <id_country>3</id_country>
            <id_state></id_state>
            <alias>Olena</alias>
            <company>Projector</company>
            <lastname>Mishchenko</lastname>
            <firstname>Olena</firstname>
            <vat_number></vat_number>
            <address1>Ukraine, Kiev</address1>
            <address2>Poland</address2>
            <postcode>02000</postcode>
            <city>Kiev</city>
            <other></other>
            <phone>097000000000</phone>
            <phone_mobile></phone_mobile>
            <dni></dni>
            <deleted></deleted>
            <date_add></date_add>
            <date_upd></date_upd>
        </address>
    </prestashop>
    """


def update_xml_body(id_address):
    return f"""
    <prestashop
        xmlns:xlink="http://www.w3.org/1999/xlink">
        <address>
            <id>{id_address}</id>
            <id_customer></id_customer>
            <id_manufacturer></id_manufacturer>
            <id_supplier></id_supplier>
            <id_warehouse></id_warehouse>
            <id_country>3</id_country>
            <id_state></id_state>
            <alias>Olena</alias>
            <company>Projector</company>
            <lastname>Mishchenko-new</lastname>
            <firstname>Olena</firstname>
            <vat_number></vat_number>
            <address1>USA</address1>
            <address2>Poland</address2>
            <postcode>88888</postcode>
            <city>Miami</city>
            <other></other>
            <phone>097000000000</phone>
            <phone_mobile></phone_mobile>
            <dni></dni>
            <deleted></deleted>
            <date_add></date_add>
            <date_upd></date_upd>
        </address>
    </prestashop>
    """

def test_can_create_address():
    # ------create address -----
    request_data = create_xml_body()
    response_create = requests.post(ENDPOINT + '/addresses', auth=(key, ""),
                                    headers={"Content-Type": "application/xml"}, data=request_data)
    assert response_create.status_code == 201

    # ------- get address -------
    response_create_data = xmltodict.parse(response_create.text)
    id_address = response_create_data['prestashop']['address']['id']

    response_get = requests.get(ENDPOINT + '/addresses/' + id_address, auth=(key, ""))
    assert response_get.status_code == 200

    response_get_data = xmltodict.parse(response_get.text)

    last_name_from_create = response_create_data['prestashop']['address']['lastname']
    last_name_from_get = response_get_data['prestashop']['address']['lastname']

    assert last_name_from_create == last_name_from_get


def test_can_update_address():

    # ------create address -----
    request_data = create_xml_body()
    response_create = requests.post(ENDPOINT + '/addresses', auth=(key, ""),
                                    headers={"Content-Type": "application/xml"}, data=request_data)
    assert response_create.status_code == 201

    # ------update address ------
    response_create_data = xmltodict.parse(response_create.text)
    id_address = response_create_data['prestashop']['address']['id']
    print(id_address)
    #
    request_data = update_xml_body(id_address)
    response_update = requests.put(ENDPOINT + '/addresses/', auth=(key, ""),
                                   headers={"Content-Type": "application/xml"}, data=request_data)

    assert response_update.status_code == 200
    print(response_update.text)

    #------ verify address --------
