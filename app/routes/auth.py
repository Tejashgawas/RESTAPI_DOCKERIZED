from flask import Blueprint,request,url_for,redirect,session,make_response
from marshmallow import ValidationError
from app.models.user import User
from app.schemas.auth_schema import RegisterSchema,LoginSchema
from app.utils.jwt_helper import generate_token,decode_token,generate_refresh_token,InvalidTokenError,ExpiredTokenError
from app.utils.response import success_response,error_response
from app import bcrypt,db
import uuid
from app.utils.oauth import oauth
import os
from flask import current_app
from flasgger import swag_from
from app.utils.redis_client import redis_client as r

  # Should print redis.client.Redis




auth_bp = Blueprint("auth_bp",__name__,url_prefix = "/auth")

register_schema = RegisterSchema()
login_schema = LoginSchema()

# ---Register--
@auth_bp.route("/register",methods = ["POST"])
@swag_from({
    'tags': ['Auth'],
    'consumes': ['application/json'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string', 'example': 'tejash123'},
                    'email': {'type': 'string', 'example': 'tejash@example.com'},
                    'password': {'type': 'string', 'example': 'strongpassword'}
                },
                'required': ['username', 'email', 'password']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'User registered successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'token': {'type': 'string'},
                    'user': {'type': 'object'}
                }
            }
        },
        400: {'description': 'Validation error'},
        409: {'description': 'Username or email already exists'}
    }
})
def register():
    try:
        data = register_schema.load(request.get_json())
    except ValidationError as err:
        return error_response(err.messages,400)
    
    #duplicates

    if User.query.filter_by(username=data['username']).first():
        return error_response("username already exist",409)
    if User.query.filter_by(email=data["email"]).first():
        return error_response("email already exist",409)
    
    user= User(**data)
    db.session.add(user)
    db.session.commit()

    token = generate_token(user.id)
    
    return success_response({"token":token,"user":user.to_dict()},"user regostered",201)


#login

@auth_bp.route("/login",methods = ["POST"])
@swag_from({
    'tags': ['Auth'],
    'summary': 'Login a user and return access & refresh tokens',
    'description': 'User must provide a valid username and password to receive JWT tokens.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {
                        'type': 'string',
                        'example': 'tejash123'
                    },
                    'password': {
                        'type': 'string',
                        'example': 'strongpassword'
                    }
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Login successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'access_token': {'type': 'string'},
                    'refresh_token': {'type': 'string'},
                    'message': {'type': 'string'}
                }
            }
        },
        401: {
            'description': 'Invalid username or password'
        },
        400: {
            'description': 'Validation failed (e.g., missing fields)'
        }
    }
})
def login():
    try:
        
        creds = login_schema.load(request.get_json())
    except ValidationError as err:
        return error_response(err.messages,400)
    
    user = User.query.filter_by(username = creds["username"]).first()
    if not user or not user.verify_password(creds["password"]):
        return error_response("invalid credentials",401)
    
    token = generate_token(user.id)
    refresh_token = generate_refresh_token(user.id)
     # ✅ Base payload
    payload = {
        "user": user.to_dict()
    }
    # ✅ Expose token in JSON during testing only
    if current_app.config["TESTING"]:
        payload["token"] = token
        payload["refresh_token"] = refresh_token
        return payload
    
    print("DEBUG: About to set refresh token in Redis")
    print("DEBUG: Type of r =", type(r))
    # Store refresh token in Redis
    r.setex(f"refresh:{user.id}", 300, refresh_token)
    response = make_response(success_response({
        "user": user.to_dict()
    }, "Login successful", 200))
    # Set secure cookies
    response.set_cookie("access_token", token, httponly=True, secure=True, samesite='Strict', max_age=300)
    response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, samesite='Strict', max_age=86400)


    return response

# ---------- Decorator to protect routes ----------

from functools import wraps
from flask import request

def token_required(fn):
    @wraps(fn)
    def wrapper(*args,**kwargs):
        auth_header = request.headers.get("Authorization", None)
        token = None

        if auth_header and auth_header.lower().startswith("bearer"):
            token = auth_header.split(" ")[1]
        else:
            token = request.cookies.get("access_token")
        if not token:
            return error_response("Access token missing", 401)
        
        

        try:
            payload = decode_token(token)
        except ExpiredTokenError:
            return error_response("Token expired", 401)
        except InvalidTokenError:
            return error_response("Token is invalid", 401)


        if not payload or payload.get("type") != "access":
            return error_response("token expired or invalid",401)
        
        
        request.user_id = payload["sub"]
        return fn(*args,**kwargs)
    
    return wrapper

# ---------- Protected profile ----------
@auth_bp.route("/profile", methods=["GET"])
@swag_from({
    'tags': ['Auth'],
    'summary': 'Get user profile',
    'security': [{'BearerAuth': []}],
    'responses': {
        200: {
            'description': 'User profile fetched successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'object'
                    },
                    'message': {'type': 'string'}
                }
            }
        },
        401: {'description': 'Unauthorized or token missing/invalid'}
    }
})
@token_required
def profile():
    user = db.session.get(User, request.user_id)
    return success_response(user.to_dict(), "Profile fetched", 200)


#refresh token

@auth_bp.route("/refresh",methods = ["GET"])
@swag_from({
    'tags': ['Auth'],
    'summary': 'Refresh access token using refresh token (cookie)',
    'responses': {
        200: {
            'description': 'New access token issued',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        },
        401: {'description': 'Invalid or expired refresh token'}
    }
})
def refresh():
    refresh_token = request.cookies.get("refresh_token")
    
    if not refresh_token:
        return error_response("Refresh token missing", 401)
    # auth_header = request.headers.get("Authorization", None)

    # if not auth_header or not auth_header.lower().startswith("bearer "):
    #     return error_response("Refresh token missing", 400)

    # refresh_token = auth_header.split()[1]
    
    try:
        payload = decode_token(refresh_token)
        if not payload:
            return error_response("Invalid or expired refresh token", 401)
        if payload['type'] != "refresh":
            return error_response("Invalid token type", 401)

        
        user_id = payload['sub']


        #compare with redis stored tokens
        stored_token = r.get(f"refresh:{user_id}")
        if stored_token and isinstance(stored_token, bytes):
            stored_token = stored_token.decode()

        if not stored_token or stored_token != refresh_token:
            return error_response("Invalid or expired refresh token", 401)

        ##issue a new access token
        new_token = generate_token(user_id)
        response = make_response(success_response(None, "Access token refreshed", 200))
        response.set_cookie("access_token", new_token, httponly=True, secure=True, samesite='Strict', max_age=300)
        return response
    except Exception as e:
        return error_response(str(e),401)
    


# Google Login Route
@auth_bp.route("/google-login")
@swag_from({
    'tags': ['Auth'],
    'summary': 'Redirect to Google OAuth login',
    'responses': {
        302: {'description': 'Redirects to Google login page'}
    }
})
def google_login():
    nonce = uuid.uuid4().hex
    session['nonce'] = nonce
    redirect_uri = url_for('auth_bp.google_callback',_external=True)
    return oauth.google.authorize_redirect(redirect_uri,nonce = nonce)

# Google Callback Route
@auth_bp.route("/google/callback")
@swag_from({
    'tags': ['Auth'],
    'summary': 'Google OAuth callback',
    'responses': {
        200: {
            'description': 'Google login successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'access_token': {'type': 'string'},
                    'refresh_token': {'type': 'string'},
                    'user': {'type': 'object'}
                }
            }
        },
        401: {'description': 'OAuth failure'}
    }
})
def google_callback():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.parse_id_token(token, nonce=session['nonce'])

    #check if user exists
    user = User.query.filter_by(email=user_info["email"]).first()

    if not user:
        user = User(
            username=user_info["name"],
            email=user_info["email"],
            password=None
        )
    
        db.session.add(user)
        db.session.commit()
    
    access_token = generate_token(user.id)
    refresh_token = generate_refresh_token(user.id)
    r.setex(f"refresh:{user.id}", 300,refresh_token)

    response = make_response( success_response({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict()
        }, "Google login successful", 200))
    
    # Set secure cookies
    response.set_cookie("access_token", access_token, httponly=True, secure=False, samesite='Strict', max_age=300)
    response.set_cookie("refresh_token", refresh_token, httponly=True, secure=False, samesite='Strict', max_age=86400)

    return response
    
    

#logout auth

@auth_bp.route("/logout", methods=["POST"])
@swag_from({
    'tags': ['Auth'],
    'summary': 'Logout user by deleting refresh token',
    'responses': {
        200: {'description': 'Logged out successfully'},
        400: {'description': 'Refresh token missing'},
        401: {'description': 'Invalid token'}
    }
})
def logout():
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        return error_response("Refresh token missing", 400)

    payload = decode_token(refresh_token)

    if not payload or payload.get("type") != "refresh":
        return error_response("Invalid token", 401)

    user_id = payload["sub"]
    r.delete(f"refresh:{user_id}")

    return success_response(None, "Logged out successfully", 200)
