# app/services/oauth_service.py
"""Google OAuth 2.0 / OpenID Connect integration using Authlib."""

from authlib.integrations.flask_client import OAuth

oauth = OAuth()


def init_oauth(app):
    """Initialize the OAuth client with the Flask app."""
    oauth.init_app(app)
    oauth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={
            "scope": "openid email profile",
        },
    )
