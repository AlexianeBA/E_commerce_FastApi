import requests


def test_get_products_with_valid_token():
    url = "http://localhost:8000/products"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEzLCJ1c2VybmFtZSI6Im9saXZlIiwicm9sZSI6ImRlYWxlciIsImV4cCI6MTcxMjgyMDc1Mn0.LHezSkgn0c1umQvW2NbrMHkAKLbEDjiWFeqREJeGyDw"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)

    print(response.text)

    assert response.status_code == 200
