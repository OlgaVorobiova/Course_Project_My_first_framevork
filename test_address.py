import pytest
import requests
import xmltodict


ENDPOINT = "http://164.92.218.36:8080/api/addresses/"
key = "1VQDHXQ8EF73QTHESPT7UHU9AJQPLXXL"

def test_get_addresses():
    response = requests.get(ENDPOINT, auth=(key, ""))
    assert response.status_code == 200
    
def create_xml_body():
    return """
    <prestashop
        xmlns:xlink="http://www.w3.org/1999/xlink">
        <address>
            <id></id>
            <id_manufacturer></id_manufacturer>
            <id_supplier></id_supplier>
            <id_warehouse></id_warehouse>
            <id_country>2</id_country>
            <id_state></id_state>
            <alias>svitlana</alias>
            <company></company>
            <lastname>Koval</lastname>
            <firstname>Svitlana</firstname>
            <vat_number></vat_number>
            <address1>Pryportova 22</address1>
            <address2></address2>
            <postcode>18016</postcode>
            <city>Cherkasy</city>
            <other></other>
            <phone></phone>
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
            <id_manufacturer></id_manufacturer>
            <id_supplier></id_supplier>
            <id_warehouse></id_warehouse>
            <id_country>2</id_country>
            <id_state></id_state>
            <alias>svitlana</alias>
            <company></company>
            <lastname>Koval</lastname>
            <firstname>Svitlana</firstname>
            <vat_number></vat_number>
            <address1>Pryportova 22</address1>
            <address2></address2>
            <postcode>18016</postcode>
            <city>Cherkasy</city>
            <other></other>
            <phone></phone>
            <phone_mobile></phone_mobile>
            <dni></dni>
            <deleted></deleted>
            <date_add></date_add>
            <date_upd></date_upd>
        </address>
    </prestashop>
    """


def test_can_create_address():
    # ---- create address ----
    request_data = create_xml_body()
    response_create = requests.post(ENDPOINT, auth=(key, ""), headers={"Content-Type": "application/xml"},
                                    data=request_data)
    assert response_create.status_code == 201
    
# ---- get id address ----
    response_create = xmltodict.parse(response_create.text)
    created_id_address = response_create['prestashop']['address']['id']
   

def test_can_update_address():
    # ---- create address ----
    request_data = create_xml_body()
    response_create = requests.post(ENDPOINT, auth=(key, ""), headers={"Content-Type": "application/xml"},
                                    data=request_data)
    assert response_create.status_code == 201
    
    # ---- update address ----
    response_create_data = xmltodict.parse(response_create.text)
    id_address = response_create_data['prestashop']['address']['id']

    request_data = update_xml_body(id_address)
    response_update = requests.put(ENDPOINT + '/' + id_address, auth=(key, ""),
                                   headers={"Content-Type": "application/xml"}, data=request_data)

    assert response_update.status_code == 200

    
def test_can_delete_address():
    # ---- create address ----
    request_data = create_xml_body()
    response_create = requests.post(ENDPOINT, auth=(key, ""), headers={"Content-Type": "application/xml"},
                                    data=request_data)
    assert response_create.status_code == 201

    # ---- delete address ----
    response_create = xmltodict.parse(response_create.text)
    id_address = response_create['prestashop']['address']['id']

    response_get = requests.delete(ENDPOINT + '/' + id_address, auth=(key, ""),
                                   headers={"Content-Type": "application/xml"}, data=request_data)
    assert response_get.status_code == 200

    # ---- get address ----
    response_get = requests.delete(ENDPOINT + '/' + id_address, auth=(key, ""),
                                headers={"Content-Type": "application/xml"}, data=request_data)
    assert response_get.status_code == 404


    
