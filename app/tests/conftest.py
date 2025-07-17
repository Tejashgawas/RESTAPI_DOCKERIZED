import pytest
from app import create_app
from app import db
from app.models.user import User
from app.utils.jwt_helper import generate_refresh_token,generate_token

@pytest.fixture
def app():
    app = create_app(testing = True)

    #create a test context
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_token(client,app):
    with app.app_context():
        res = client.post("auth/register",json={
            "username" : "test1",
            "email" : "test1@example.com",
            "password" : "test123"
        })
        print("Register Response:", res.json)
        print("Status Code:", res.status_code)

        reponse = client.post("/auth/login",json={
            "username" : "test1",
            "password" : "test123"
        })
        print("Login Response JSON:", reponse.json)
        print("Status Code:", reponse.status_code)


        token = reponse.json["token"]
        return token

@pytest.fixture
def tokens():
    user = User(username="test1", email="test1@example.com", password="test123")
    db.session.add(user)
    db.session.commit()
    access = generate_token(user.id)
    refresh = generate_refresh_token(user.id)
    return {"access": access, "refresh": refresh}
