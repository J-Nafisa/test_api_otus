import pytest
import requests
import json

expected_params = [
    "id",
    "postId",
    "email",
    "body",
    "name"
]

# 1. Тест для "Creating a resource" проверяет создание записи, корректностьи кода и сверяет данные из респонса.
@pytest.mark.parametrize("title, body, userId", [
    ("nafisa", "test api nafisapi", "13"),
    ("example", "test api example", "42"),
    ("foo", "test api foo", "99")
])
def test_create_entity(title, body, userId):
    url = 'https://jsonplaceholder.typicode.com/posts'
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    payload = {
        "title": title,
        "body": body,
        "userId": userId
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    assert response.status_code == 201
    response_body = response.json()
    assert response_body["title"] == title
    assert response_body["body"] == body
    assert response_body["userId"] == userId
    assert "id" in response_body



# 2. Тест для "Updating a resource" проверяет создание записи, корректностьи кода и сверяет данные из респонса.
@pytest.mark.parametrize("id, title, body, userId", [
    (1, "nafisa_1", "test api nafisapi_1", "13_1"),
    (2, "example_2", "test api example_2", "42_2"),
    (3, "foo_3", "test api foo_3", "99_3")
])
def test_update_entity(id, title, body, userId):
    url = f'https://jsonplaceholder.typicode.com/posts/{id}'
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    payload = {
        "id": id,
        "title": title,
        "body": body,
        "userId": userId
    }

    response = requests.put(url, headers=headers, data=json.dumps(payload))

    assert response.status_code == 200
    response_body = response.json()
    assert response_body["id"] == id
    assert response_body["title"] == title
    assert response_body["body"] == body
    assert response_body["userId"] == userId

# 3. Тест для "Listing nested resources" проверяет записи в ответе на наличие необходимых переменных.
def test_get_comments():
    url = 'https://jsonplaceholder.typicode.com/posts/1/comments'

    response = requests.get(url)
    assert response.status_code == 200

    comments = response.json()
    assert isinstance(comments, list)
    assert len(comments) > 0

    for comment in comments:
        for param in expected_params:
            assert param in comment

# 4. Тест для "Listing nested resources" проверяет наличие значений параметров и их форму.
def test_comment_parameter_values():
    url = 'https://jsonplaceholder.typicode.com/posts/1/comments'

    response = requests.get(url)
    assert response.status_code == 200

    comments = response.json()
    assert isinstance(comments, list)
    assert len(comments) > 0

    for comment in comments:
        assert isinstance(comment["id"], int)
        assert isinstance(comment["postId"], int)
        assert isinstance(comment["email"], str)
        assert isinstance(comment["body"], str)
        assert isinstance(comment["name"], str)

        assert comment["postId"] > 0
        assert len(comment["email"]) > 0
        assert len(comment["name"]) > 0
        assert comment["id"] > 0


# 5. Тест для "Deleting a resource" на успешное удаление ресурса.
def test_delete_resource():
    url = 'https://jsonplaceholder.typicode.com/posts/1'
    headers = {'Content-Type': 'application/json'}
    payload = {"id": 101}

    response = requests.delete(url, headers=headers, data=json.dumps(payload))

    assert response.status_code == 200
    assert response.text == '{}'

if __name__ == '__main__':
    pytest.main()


