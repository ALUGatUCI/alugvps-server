from pydantic import BaseModel

class ConfirmationCode(BaseModel):
    code: str

class ContainerRequest(BaseModel):
    request_body: str