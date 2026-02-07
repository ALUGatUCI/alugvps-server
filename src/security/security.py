from typing import Annotated

import jwt
from fastapi import HTTPException, status, Depends
import fastapi.security as security
from jwt import InvalidTokenError
from pwdlib import PasswordHash

SECRET_KEY = "46810de1ffee764917b80678b169d1b829ceda1b2ddd0a8e01b88cb01902dbf9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hasher = PasswordHash.recommended()
oauth2_scheme = security.OAuth2PasswordBearer(tokenUrl="token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def verify_credentials(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise credentials_exception

        ucinetid = email[:payload.get("sub").index("@")]

    except InvalidTokenError:
        raise credentials_exception

    return ucinetid