from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
import sqlmodel
import jwt
from security import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, password_hasher as ph, ALGORITHM
from database.models import AccountCreation, Account
import database.database as database
import database.containers as containers
import database.exceptions as exceptions
import asyncio

class Token(BaseModel):
    access_token: str
    token_type: str

def _create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create an access token"""
    to_encode = data.copy()
    if expires_delta:
        expires = datetime.now(timezone.utc) + expires_delta
    else:
        expires = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

async def add_account_to_database(account: AccountCreation):
    """Create an account and add it to the database"""

    # Start by hashing the password
    hashed_password = await asyncio.to_thread(ph.hash, account.password.get_secret_value()) # Run in async thread to prevent block

    # Get the database session
    session = database.session

    # Create the account with the Account class
    new_account = Account(
        email = account.email,
        password = hashed_password,
        confirmed = False,
        banned = False
    )

    session.add(new_account)
    session.commit()
    session.refresh(new_account)

    # Now create the associated container
    await containers.create_new_container(new_account.id, account)

def perform_login(email: str, password: str):
    """Perform a login and return a token"""
    session = database.session # Get the session

    statement = sqlmodel.select(Account).where(email == Account.email) # See if an account with that email exists
    result = session.exec(statement).first()

    if result is None: # If it doesn't, raise an error
        raise exceptions.AccountNotFoundError(email)

    # If an account was found, we check the password matches
    if ph.verify(password, result.password):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = _create_access_token(
            {"sub" : result.email}, expires_delta=access_token_expires
        )
    else:
        raise exceptions.InvalidPasswordError()

    return Token(access_token=access_token, token_type="bearer")