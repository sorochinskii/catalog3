def test_check_openapijson(test_client):
    response = test_client.get('/openapi.json')
    assert response.status_code == 200
