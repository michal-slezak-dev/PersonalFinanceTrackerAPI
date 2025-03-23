import bcrypt
import os
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    return str(hashed_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def create_access_token(data: dict, expires_delta: timedelta=timedelta(hours=1)) -> str:
    data_to_encode = data.copy()
    expire = datetime.now() + expires_delta
    data_to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise jwt.PyJWTError
