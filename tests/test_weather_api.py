import json

from codes import temp_test


def test_weather_response_shape_and_ranges():
    client = temp_test.app.test_client()
    resp = client.get('/weather?city=Bangalore&country=IN')
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'temperature_celsius' in data
    assert 'humidity_percent' in data
    temp = data['temperature_celsius']
    humid = data['humidity_percent']
    # types
    assert isinstance(temp, (int, float))
    assert isinstance(humid, (int, float))
    # realistic ranges
    assert -10 <= temp <= 50
    assert 0 <= humid <= 100
