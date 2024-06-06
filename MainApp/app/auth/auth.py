import os

from dotenv import load_dotenv
from fastapi_users.authentication import CookieTransport, AuthenticationBackend, JWTStrategy

cookie_transport = CookieTransport(cookie_max_age=10000)

load_dotenv()

SECRET = os.getenv("SECRET")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=10000)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
