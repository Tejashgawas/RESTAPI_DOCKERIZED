from authlib.integrations.flask_client import OAuth
from flask import current_app


oauth = OAuth()

def configure_oauth(app):
    oauth.init_app(app)

    #google Oauth config
    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET_KEY'],
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }

    )

