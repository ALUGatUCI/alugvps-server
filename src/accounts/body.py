from pydantic import BaseModel

class AccountCreationBody(BaseModel):
    email: str
    password: str