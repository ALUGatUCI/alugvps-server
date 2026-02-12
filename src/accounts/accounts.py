import string
from typing import Annotated

import fastapi
from fastapi import Depends
from database import containers
from database import Container
from database.accounts import Account, add_account_to_database, perform_login
from database.models import AccountCreation
import database.database as database
import database.exceptions as db_exceptions
from configuration import configuration
import sqlmodel
from sqlmodel import select, delete
from sqlalchemy import func
from accounts.body import ConfirmationCode

from security import oauth2_scheme, verify_credentials

router = fastapi.APIRouter()

@router.post("/confirm")
async def confirm_account(token: Annotated[str, fastapi.Depends(oauth2_scheme)], inputted_code: ConfirmationCode = Depends()):
    ucinetid = verify_credentials(token)

    session = database.session

    statement = sqlmodel.select(Account).where(Account.email == f"{ucinetid}@uci.edu")
    result = session.execute(statement).first()[0]

    if result is None:
        raise fastapi.HTTPException(status_code=400, detail="Account not found")

    if result.confirmed == True:
        raise fastapi.HTTPException(status_code=400, detail="Account is already confirmed")

    if result.confirmation_code != inputted_code.code:
        raise fastapi.HTTPException(status_code=400, detail="Incorrect confirmation code")

    # Assuming all checks pass, changed their confirmed status and create container
    result.confirmed = True
    session.commit()

    # Try to create the container
    try:
        await containers.create_new_container(result.id, result)
    except:
        # If it already exists, let it be
        pass

    return fastapi.Response(status_code=201)

@router.post("/create_account")
async def create_account(account: AccountCreation = Depends()):
    """Do the password creation logic"""

    # Check if there is anymore space for accounts
    if configuration.read_config_file("acc_limit") is not None:
        statement = select(func.count()).select_from(Account)
        result = database.session.execute(statement).one()[0]

        if result >= configuration.read_config_file("acc_limit"):
            raise fastapi.HTTPException(status_code=400, detail="Account limit on server reached")

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
    if account.password.get_secret_value().strip() == "":
        raise fastapi.HTTPException(status_code=400, detail="Password is required")

    if len(account.password) < 8:
        raise fastapi.HTTPException(status_code=400, detail="Password is too short")

    if not any(c.islower() for c in account.password.get_secret_value()):
        raise fastapi.HTTPException(
            status_code=400,
            detail="Password must contain at least one lowercase character"
        )

    if not any(c.isupper() for c in account.password.get_secret_value()):
        raise fastapi.HTTPException(
            status_code=400,
            detail="Password must contain at least one uppercase character"
        )

    if not any(c.isdigit() for c in account.password.get_secret_value()):
        raise fastapi.HTTPException(
            status_code=400,
            detail="Password must contain at least one digit"
        )

    if not any(c in string.punctuation for c in account.password.get_secret_value()):
        raise fastapi.HTTPException(
            status_code=400,
            detail="Password must contain at least one punctuation"
        )

    try:
        await add_account_to_database(account)
    except Exception as e:
        # Do the cleanup work if necessary
        acc_statement = select(Account).where(Account.email == account.email)
        account_entry = session.execute(acc_statement).first()[0]

        if account_entry is not None:
            account_id = account_entry.id
            rm_acc_statement = delete(Account).where(Account.id == account_id)
            session.execute(rm_acc_statement)
            session.commit()

        con_statement = select(Container).where(Container.id == account_id)
        con_entry = session.execute(con_statement).first()[0]

        if con_entry is not None:
            rm_con_statement = delete(Container).where(Container.id == account_id)
            session.execute(rm_con_statement)
            session.commit()

        # Raise the API exception
        raise fastapi.HTTPException(status_code=500, detail=str(e))

    return fastapi.Response(status_code=201)

def login_to_account(username, password) -> str:
    """Do the login logic"""
    try:
        return perform_login(username, password)
    except db_exceptions.AccountNotFoundError as e:
        raise fastapi.HTTPException(status_code=401, detail=str(e))
    except db_exceptions.InvalidPasswordError as e:
        raise fastapi.HTTPException(status_code=401, detail=str(e))