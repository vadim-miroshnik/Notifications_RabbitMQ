from http import HTTPStatus

from models.user import User


def test_1(client, db_session):
    user = User(
        login="test_user",
        password="password",
        email="testuser@example.com",
        fullname="fullname",
        phone="+79627950693",
    )
    db_session.add(user)
    db_session.commit()
    user = db_session.query(User).filter_by(login="test_user").all()[0]
    print(user.id)
    print(user.allow_send_email)
    #response = client.post("/login")
    data = {
        "user_id": user.id,
    }
    response = client.get("/login", params=data)
    print(response.json())
    assert response.status_code == HTTPStatus.OK
    assert "access_token" in response.json()
    acess_token = response.json()['access_token']
    print(acess_token)
    assert True
    response = client.get("/enable-notifications", headers={"Authorization": f"Bearer {acess_token}"})
    assert response.status_code == HTTPStatus.OK
    user = db_session.query(User).filter_by(login="test_user").all()[0]
    print(user.allow_send_email)
    assert user.allow_send_email