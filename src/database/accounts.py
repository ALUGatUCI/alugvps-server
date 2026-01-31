import sqlmodel
from argon2 import PasswordHasher
from typing import Optional
import accounts.body
import database.database as database
import asyncio

class Account(sqlmodel.SQLModel, table=True):
    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    email: str = sqlmodel.Field(index=True, unique=True)
    password: str
    confirmed: bool = sqlmodel.Field(default=False)
    banned: bool = sqlmodel.Field(default=False)

def create_account(account: accounts.body.AccountCreationBody):
    """Create an account and add it to the database"""

    # Start by hashing the password
    ph = PasswordHasher()
    hashed_password = asyncio.to_thread(ph.hash, account.password) # Run in async thread to prevent block

    # Get the database session
    session = database.get_session()

    # Create the account with the Account class
    new_account = Account(
        email = account.email,
        password = hashed_password,
    )

    session.add(new_account)
    session.commit()
    session.refresh(new_account)