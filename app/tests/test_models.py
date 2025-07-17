from app.models.user import User
from app import db

def test_create_user(app):
    with app.app_context():
        user = User(username="Test",email = "test@example.com",password=None)

        db.session.add(user)
        db.session.commit()

        saved_user = User.query.filter_by(email = "test@example.com").first()

        assert saved_user is not None
        assert saved_user.email == "test@example.com"
        
