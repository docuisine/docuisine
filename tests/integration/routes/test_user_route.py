def test_create_user(client):
    user_data = {
        "username": "testuser",
        "password": "123Password!",
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["username"] == user_data["username"]
    assert "id" in data


def test_get_user(client):
    # First, create a user to retrieve
    user_data = {
        "username": "anotheruser",
        "password": "456Password!",
    }
    create_response = client.post("/users/", json=user_data)
    assert create_response.status_code == 201, create_response.text
    created_user = create_response.json()
    user_id = created_user["id"]
    # Now, retrieve the user by ID
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 200, get_response.text
    retrieved_user = get_response.json()
    assert retrieved_user["id"] == created_user["id"]
    assert retrieved_user["username"] == created_user["username"]
