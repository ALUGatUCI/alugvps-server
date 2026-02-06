from pydantic import BaseModel

class ListContainers(BaseModel):
    success: bool
    containers: list

class ContainerStatus(BaseModel):
    success: bool
    status: str

class ContainerAction(BaseModel):
    success: bool
    message: str