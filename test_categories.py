import requests
import xmltodict

key = "1VQDHXQ8EF73QTHESPT7UHU9AJQPLXXL"
ENDPOINT = "http://164.92.218.36:8080/api/categories"


def test_can_get_categories():
    response = requests.get(ENDPOINT, auth=(key, ""))
    assert response.status_code == 200
    

def create_xml_body():
    return """
    <prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
        <category>
            <id_parent></id_parent>
            <active>1</active>
            <id_shop_default></id_shop_default>
            <is_root_category></is_root_category>
            <position></position>
            <date_add></date_add>
            <date_upd></date_upd>
            <name>
                <language id="1" xlink:href="http://164.92.218.36:8080/api/languages/1">Vine</language>
            </name>
            <link_rewrite>
                <language id="1" xlink:href="http://164.92.218.36:8080/api/languages/1"></language>
            </link_rewrite>
            <description>
                <language id="1" xlink:href="http://164.92.218.36:8080/api/languages/1"></language>
            </description>
            <meta_title>
                <language id="1" xlink:href="http://164.92.218.36:8080/api/languages/1"></language>
            </meta_title>
            <meta_description>
                <language id="1" xlink:href="http://164.92.218.36:8080/api/languages/1"></language>
            </meta_description>
            <meta_keywords>
                <language id="1" xlink:href="http://164.92.218.36:8080/api/languages/1"></language>
            </meta_keywords>
            <associations>
                <categories nodeType="category" api="categories"/>
                <products nodeType="product" api="products"/>
            </associations>
        </category>
    </prestashop>
    """


def update_xml_body(created_id_category):
    return f"""
    <prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
        <category>
            <id>{created_id_category}</id>
            <id_parent></id_parent>
            <active>1</active>
            <id_shop_default></id_shop_default>
            <is_root_category></is_root_category>
            <position></position>
            <date_add></date_add>
            <date_upd></date_upd>
            <name>
                <language id="1" xlink:href="http://164.92.218.36:8080/api/languages/1">Lemonade</language>
            </name>
            <link_rewrite>
                <language id="1" xlink:href="http://164.92.218.36:8080/api/languages/1"></language>
            </link_rewrite>
            <description>
                <language id="1" xlink:href="http://164.92.218.36:8080/api/languages/1"></language>
            </description>
            <meta_title>
                <language id="1" xlink:href="http://164.92.218.36:8080/api/languages/1"></language>
            </meta_title>
            <meta_description>
                <language id="1" xlink:href="http://164.92.218.36:8080/api/languages/1"></language>
            </meta_description>
            <meta_keywords>
                <language id="1" xlink:href="http://164.92.218.36:8080/api/languages/1"></language>
            </meta_keywords>
            <associations>
                <categories nodeType="category" api="categories"/>
                <products nodeType="product" api="products"/>
            </associations>
        </category>
    </prestashop>
    """


def test_can_create_category():
    # ---- create category ----
    request_data = create_xml_body()
    response_create = requests.post(ENDPOINT, auth=(key, ""), headers={"Content-Type": "application/xml"},
                                    data=request_data)
    assert response_create.status_code == 201

    # ---- get id category ----
    response_create = xmltodict.parse(response_create.text)
    created_id_category = response_create['prestashop']['category']['id']
    


def test_can_update_category():
    # ---- create category ----
    request_data = create_xml_body()
    response_create = requests.post(ENDPOINT, auth=(key, ""), headers={"Content-Type": "application/xml"},
                                    data=request_data)
    assert response_create.status_code == 201

    # ---- update category ----
    response_create_data = xmltodict.parse(response_create.text)
    id_category = response_create_data['prestashop']['category']['id']

    request_data = update_xml_body(id_category)
    response_update = requests.put(ENDPOINT + '/' + id_category, auth=(key, ""),
                                   headers={"Content-Type": "application/xml"}, data=request_data)

    assert response_update.status_code == 405

    # ---- get category ----
    response_get = requests.get(ENDPOINT + '/' + id_category, auth=(key, ""),
                                headers={"Content-Type": "application/xml"}, data=request_data)
    assert response_get.status_code == 200


def test_can_delete_category():
    # ---- create category ----
    request_data = create_xml_body()
    response_create = requests.post(ENDPOINT, auth=(key, ""), headers={"Content-Type": "application/xml"},
                                    data=request_data)
    assert response_create.status_code == 201

    # ---- delete category ----
    response_create = xmltodict.parse(response_create.text)
    id_category = response_create['prestashop']['category']['id']

    response_get = requests.delete(ENDPOINT + '/' + id_category, auth=(key, ""),
                                   headers={"Content-Type": "application/xml"}, data=request_data)
    assert response_get.status_code == 405

    # ---- get category ----
    response_get = requests.get(ENDPOINT + '/' + id_category, auth=(key, ""),
                                headers={"Content-Type": "application/xml"}, data=request_data)
    assert response_get.status_code == 200
