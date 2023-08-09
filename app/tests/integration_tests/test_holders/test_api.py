import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "username,password,email,age,status_code",
    [
        ("User2000", "password", "test@example.com", 28, 200),
        ("User2e0", "password", "tccxcxcxxcm", 28, 422),
        ("User2000", "password", "test@example.com", 28, 409),
    ],
)
async def test_register_user1(
    username, password, email, age, status_code, ac: AsyncClient
):
    response = await ac.post(
        "/holders/register",
        json={"username": username, "password": password, "email": email, "age": age},
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    " email,password,status_code",
    [
        ("tech@ninja.com", "string", 200),
        ("tech@ninja2.com", "password", 401),
    ],
)
async def test_login(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/holders/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == status_code


# async def test_register_user1(ac: AsyncClient):
#     response =  await ac.post("/holders/register", json={
#         "username": "newUser",
#         "password": "string",
#         "email": "test@example.com",
#         "age": 28

#     })

#     assert response.status_code == 200
