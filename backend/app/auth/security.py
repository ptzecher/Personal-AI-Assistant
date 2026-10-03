from pwdlib import PasswordHash

import os
from dotenv import load_dotenv
import jwt
from jwt.exceptions import InvalidTokenError

from datetime import datetime, timedelta, timezone

load_dotenv()

password_hash=PasswordHash.recommended()

SECRET_KEY=os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password:str)->str:
    return  password_hash.hash(password)

def verify_password(plain_password:str,hashed_password:str)->bool:
    return password_hash.verify(plain_password,hashed_password)

def create_access_token(user_id:int)->str:

    expire=(datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload={
        "sub":str(user_id),
        "exp":expire
    }
    token=jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token

def decode_access_token(token:str)->int:

    try:
        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id=payload.get('sub')

        if user_id is None:
            raise InvalidTokenError()
        return int(user_id)

    except (InvalidTokenError, ValueError):
        raise



