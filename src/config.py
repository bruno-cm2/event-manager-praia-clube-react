import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])

DOMINIO_EMPRESA = os.environ["DOMINIO_EMPRESA"]
GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]

DATABASE_URL = os.environ["DATABASE_URL"]
SQLALCHEMY_ECHO = os.environ.get("SQLALCHEMY_ECHO", "False").lower() in ("true", "1", "t")
