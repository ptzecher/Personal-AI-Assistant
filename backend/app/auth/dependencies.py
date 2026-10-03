from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from auth.security import decode_access_token
from database.database import get_db
from database.repository import get_user_by_id


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login"
)

def get_current_user(token:str=Depends(oauth2_scheme),db: Session=Depends(get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:

        user_id=decode_access_token(token)

    except (InvalidTokenError, ValueError):

        raise credentials_exception
    user=get_user_by_id(user_id=user_id,db=db)

    if user is None:
        raise credentials_exception

    return user

