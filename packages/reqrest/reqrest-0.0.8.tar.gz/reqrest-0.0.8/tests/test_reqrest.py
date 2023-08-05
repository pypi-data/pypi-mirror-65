"""Test for reqrest"""
import json
import random
import string
import reqrest

# Thanks to https://postman-echo.com
# For the demo REST API

REST = reqrest.REST(url='postman-echo.com', debug=True)


# Generate random data for testing
def random_string(string_length=15):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def test_rest_get():
    """Test GET"""
    test_param1 = random_string()
    test_param1_value = random_string()
    test_param2 = random_string()
    test_param2_value = random_string()

    query_string = {}
    query_string[test_param1] = test_param1_value
    query_string[test_param2] = test_param2_value

    response = REST.get('/get', query_string)

    assert response.status_code == 200

    response = json.loads(response.text)['args']

    assert response[test_param1] == test_param1_value
    assert response[test_param2] == test_param2_value


def test_rest_post():
    """Test POST"""
    test_title = random_string()
    test_body = random_string()
    test_user_id = random_string()

    payload = {}
    payload['title'] = test_title
    payload['body'] = test_body
    payload['userId'] = test_user_id

    response = REST.post("/post", payload)

    assert response.status_code == 200

    response = json.loads(response.text)['data']

    assert response['userId'] == test_user_id
    assert response['title'] == test_title
    assert response['body'] == test_body


def test_rest_put():
    """Test PUT"""
    test_title = random_string()
    test_body = random_string()
    test_user_id = random_string()

    payload = {}
    payload['title'] = test_title
    payload['body'] = test_body
    payload['userId'] = test_user_id

    response = REST.put("/put", payload)

    assert response.status_code == 200

    response = json.loads(response.text)['form']

    print(response)

    assert response['userId'] == test_user_id
    assert response['title'] == test_title
    assert response['body'] == test_body


def test_rest_patch():
    """Test patch"""
    test_title = random_string()
    test_body = random_string()
    test_user_id = random_string()

    payload = {}
    payload['title'] = test_title
    payload['body'] = test_body
    payload['userId'] = test_user_id

    response = REST.patch("/patch", payload)

    assert response.status_code == 200

    response = json.loads(response.text)['form']

    print(response)

    assert response['userId'] == test_user_id
    assert response['title'] == test_title
    assert response['body'] == test_body

def test_rest_delete():
    """Test DELETE"""
    response = REST.delete('/delete')
    assert response.status_code == 200


def test_response_headers():
    """Test getting response headers"""
    response = REST.response_headers('/get')

    assert response['Content-Type'] == 'application/json; charset=utf-8'
    assert response['Connection'] == 'keep-alive'
    assert response['Server'] == 'nginx'


def test_custom_header():
    """Test header override"""
    header_content = random_string()
    header_key = random_string()

    headers = {header_key: header_content}

    crest = reqrest.REST(url='postman-echo.com', headers=headers, debug=True)

    response = json.loads(crest.get('/headers').text)

    assert response['headers'][header_key] == header_content
