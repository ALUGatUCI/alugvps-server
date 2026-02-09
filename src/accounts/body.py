from pydantic import BaseModel, SecretStr

class AccountCreation(BaseModel):
    email: str
    password: SecretStr