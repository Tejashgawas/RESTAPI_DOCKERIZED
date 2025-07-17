from app import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(db.Model):
    __tablename__="users"

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(100),nullable = False,unique = True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        if password:  # only hash if it's not None
            self.password = self.generate_hash(password)
        else:
            self.password = None

    def generate_hash(self,password):
        return bcrypt.generate_password_hash(password).decode('utf-8')\
        
    def verify_password(self,password):
        return bcrypt.check_password_hash(self.password,password)
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }
    


