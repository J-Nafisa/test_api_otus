import requests
import pytest

# 1. Тест для LIST ALL BREEDS проверяет наличие определенной породы собаки в списке.
def test_get_breed():
    response = requests.get("https://dog.ceo/api/breeds/list/all")
    assert response.status_code == 200
    data = response.json()
    assert "bulldog" in data["message"]
    assert "status" in data
    assert data["status"] == "success"

# 2. Тест для LIST ALL BREEDS проверяет наличие подпороды у определенной породы собаки.
@pytest.mark.parametrize("breed, subbreed", [("bulldog", "english"), ("hound", "basset")])
def test_get_subbreed(breed, subbreed):
    response = requests.get("https://dog.ceo/api/breeds/list/all")
    assert response.status_code == 200
    data = response.json()
    assert breed in data["message"]
    assert subbreed in data["message"][breed]
    assert "status" in data
    assert data["status"] == "success"

# 3. Тест для DISPLAY SINGLE RANDOM IMAGE проверяет, что поле "message" содержит URL изображения с расширением .jpg
def test_get_random_dog_image():
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    image_url = data["message"]
    assert image_url.startswith("https://images.dog.ceo/breeds/")
    assert image_url.endswith(".jpg")
    assert "status" in data
    assert data["status"] == "success"

# 4. Тест для IMAGES FROM A BREED для проверки разных пород собак.
@pytest.mark.parametrize("breed", ["pointer", "setter", "pug", "segugio", "husky", "wolfhound"])
def test_get_random_dog_image_by_breed(breed):
    url = f"https://dog.ceo/api/breed/{breed}/images"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], list)
    for image_url in data["message"]:
        assert image_url.startswith("https://images.dog.ceo/breeds/")
        assert image_url.endswith(".jpg")
        assert "status" in data
        assert data["status"] == "success"

# 4. Тест для LIST ALL SUB-BREEDS для проверки списка разных подпород собак.
@pytest.mark.parametrize("breed", ["pointer", "setter", "pug", "segugio", "husky", "terrier", "wolfhound"])
def test_get_dog_list_subbreed_by_breed(breed):
    url = f"https://dog.ceo/api/breed/{breed}/list"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "status" in data
    assert isinstance(data["message"], list)
    assert data["status"] == "success"

# 5. Негативный тест для LIST ALL SUB-BREEDS проверяет, что, при запросе списка подпород собак по неправильно записанной или несуществующей породе, выдается ошибка.
@pytest.mark.parametrize("breed", ["random", "words", "breed", "poyntr", "seter", "pugg", "segguio", "hosky", "terier", "wolfhund"])
def test_get_dog_list_invalid_breed(breed):
    url = f"https://dog.ceo/api/breed/{breed}/list"
    response = requests.get(url)
    assert response.status_code == 404
    data = response.json()
    assert "message" in data
    assert "status" in data
    assert data["message"] == "Breed not found (master breed does not exist)"
    assert data["status"] == "error"
    assert data["code"] == 404


# Запуск тестов
if __name__ == "__main__":
    pytest.main([__file__])