from pydantic import BaseModel

class AccountLogin(BaseModel):
    email: str
    password: str

class Account(BaseModel):
    email: str | None = None
    disabled: bool | None = None