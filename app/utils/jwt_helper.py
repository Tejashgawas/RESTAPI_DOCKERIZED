import jwt ,datetime

from flask import current_app
from app.utils.response import success_response,error_response


class TokenError(Exception):
    pass

class ExpiredTokenError(TokenError):
    pass

class InvalidTokenError(TokenError):
    pass

def generate_token(user_id,expires_in = 120):

    payload = {
        "sub" :  str(user_id),
        "iat" : datetime.datetime.utcnow(),
        "exp" : datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in),
        "type":"access"

    }

    return jwt.encode(payload,current_app.config["SECRET_KEY"],algorithm="HS256")

def generate_refresh_token(user_id, expires_in=300):  # 7 days
    payload = {
        "sub": str(user_id),
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in),
        "type": "refresh"
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def decode_token(token):
    try:
        print("Refresh Token from Cookie:", token)
        payload = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        print("Token expired.")
        raise ExpiredTokenError("Token expired", 401)
    except jwt.InvalidTokenError as e:
        print("Token invalid:", str(e))
        raise InvalidTokenError("Token is invalid", 401)

    