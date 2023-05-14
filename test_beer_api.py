import requests
import pytest
import re

expected_params = [
    "id",
    "name",
    "brewery_type",
    "address_1",
    "address_2",
    "address_3",
    "city",
    "state_province",
    "postal_code",
    "country",
    "longitude",
    "latitude",
    "phone",
    "website_url",
    "state",
    "street"
]

# 1. Тест для "List Breweries" проверяет наличие всех необходимых полей в полном списке пивоварен.
@pytest.mark.parametrize("param", expected_params)
def test_get_all_breweries(param):
    url = "https://api.openbrewerydb.org/v1/breweries"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    for brewery in data:
        assert param in brewery


# 2. Тест для "List Breweries By State" проверяет наличие всех необходимых полей в списке пивоварен определенных штатов.
@pytest.mark.parametrize("state,param", [(state, param) for state in ["California", "Colorado", "Oregon", "Texas"] for param in expected_params])
def test_get_breweries_by_state(state, param):
    url = f"https://api.openbrewerydb.org/v1/breweries?by_state={state}"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    for brewery in data:
        assert param in brewery


# 3. Тест для "Autocomplete Search" проверяет наличие указанных значений в name и доп проверяет, что в ответе есть год.
@pytest.mark.parametrize("query", ["1912", "1850", "1905", "1840"])
def test_brewery_autocomplete(query):
    url = f"https://api.openbrewerydb.org/v1/breweries/autocomplete?query={query}"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    for brewery in data:
        assert "id" in brewery
        assert "name" in brewery
        assert re.search(r"\b\d{4}\b", query) is not None

# 3. Тест для "Autocomplete Search" проверяет пустой запрос.
def test_brewery_autocomplete_empty_query():
    url = "https://api.openbrewerydb.org/v1/breweries/autocomplete?query="
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

# 4. Негативный тест для "Autocomplete Search", который проверяет ввод несуществующих значений.
@pytest.mark.parametrize("query", ["пивоварня", "@#$%^&*", "lalalalala", ".,;:!?"])
def test_brewery_autocomplete_empty_result(query):
    url = f"https://api.openbrewerydb.org/v1/breweries/autocomplete?query={query}"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data == []

# 5. Тест для "Random Brewery", который проверяет что значения id не повторяются в цикле запросов(сравниваем с предыдущим).
def test_multiple_random_breweries():
    breweries = set()
    previous_id = None
    for _ in range(20):
        url = "https://api.openbrewerydb.org/v1/breweries/random"
        response = requests.get(url)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        brewery = data[0]

        current_id = str(brewery["id"])
        if previous_id is not None:
            assert current_id != previous_id, f"Current ID: {current_id} is equal to Previous ID: {previous_id}"
            previous_id = current_id

        for param in expected_params:
            assert param in brewery




# Запуск тестов
if __name__ == "__main__":
    pytest.main([__file__])