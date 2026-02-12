from typing import Annotated

from sqlmodel import select

from configuration import configuration
import jwt
from fastapi import HTTPException, status, Depends
import fastapi.security as security
from jwt import InvalidTokenError
from pwdlib import PasswordHash

from database import database
from database.models import Account

SECRET_KEY = configuration.read_config_file("secret_key")
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

def check_confirmation_status(ucinetid: str):
    session = database.session

    statement = select(Account).where(Account.email == f"{ucinetid}@uci.edu")
    result = session.execute(statement).first()[0]

    return result.confirmed