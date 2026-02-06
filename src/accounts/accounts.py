import string
import fastapi
from fastapi import Depends

from accounts.body import AccountLogin
from fastapi.security import OAuth2PasswordRequestForm
from database.accounts import Account, add_account_to_database, perform_login, Token
import database.database as database
import database.exceptions as db_exceptions
import sqlmodel
from typing import Annotated

router = fastapi.APIRouter()

@router.post("/create_account")
async def create_account(account: AccountLogin):
    """Do the password creation logic"""

    # Start with validating the emails
    if not account.email.endswith("@uci.edu"):
        raise fastapi.HTTPException(status_code=400, detail="Email address is not valid")

    # Get the database session
    session = database.session

    statement = sqlmodel.select(Account.email)
    emails = session.exec(statement).all()

    if account.email in emails:
        raise fastapi.HTTPException(status_code=400, detail="Email address already exists")

    # Now validate the password
    if account.password.strip() == "":
        raise fastapi.HTTPException(status_code=400, detail="Password is required")

    if len(account.password) < 8:
        raise fastapi.HTTPException(status_code=400, detail="Password is too short")

    if not any(c.islower() for c in account.password):
        raise fastapi.HTTPException(
            status_code=400,
            detail="Password must contain at least one lowercase character"
        )

    if not any(c.isupper() for c in account.password):
        raise fastapi.HTTPException(
            status_code=400,
            detail="Password must contain at least one uppercase character"
        )

    if not any(c.isdigit() for c in account.password):
        raise fastapi.HTTPException(
            status_code=400,
            detail="Password must contain at least one digit"
        )

    if not any(c in string.punctuation for c in account.password):
        raise fastapi.HTTPException(
            status_code=400,
            detail="Password must contain at least one punctuation"
        )

    await add_account_to_database(account)

    return fastapi.Response(status_code=201)

def login_to_account(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Do the login logic"""
    try:
        return perform_login(form_data.username, form_data.password)
    except db_exceptions.AccountNotFoundError as e:
        raise fastapi.HTTPException(status_code=401, detail=str(e))
    except db_exceptions.InvalidPasswordError as e:
        raise fastapi.HTTPException(status_code=401, detail=str(e))