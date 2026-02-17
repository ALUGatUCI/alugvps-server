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

class PortsList(BaseModel):
    success: bool
    ports: list[tuple]

class ContainerAddress(BaseModel):
    success: bool
    address: str