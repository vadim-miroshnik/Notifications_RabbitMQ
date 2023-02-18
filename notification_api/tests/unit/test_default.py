from http import HTTPStatus


def test_enable_notification(client, test_user_info):
    response = client.get(
        "/login",
        params={
            "user_id": test_user_info().id,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert "access_token" in response.json()
    acess_token = response.json()["access_token"]
    response = client.get("/enable-notifications", headers={"Authorization": f"Bearer {acess_token}"})
    assert response.status_code == HTTPStatus.OK
    assert test_user_info().allow_send_email is True
