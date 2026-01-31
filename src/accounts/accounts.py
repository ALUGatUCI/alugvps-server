import string
import fastapi
from accounts.body import AccountCreationBody
import database.accounts as account_db
import database.database as database
import sqlmodel

router = fastapi.APIRouter()

@router.post("/create_account")
def create_account(account: AccountCreationBody):
    """Do the password creation logic"""

    # Start with validating the emails
    if not account.email.endswith("@uci.edu"):
        raise fastapi.HTTPException(status_code=400, detail="Email address is not valid")

    # Get the database session
    session = database.get_session()

    statement = sqlmodel.select(account_db.Account.email)
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

    account_db.create_account(account)

    return fastapi.Response(status_code=201)