import fastapi
import jwt
from fastapi import Depends
from jwt import InvalidTokenError
from pylxd import Client
from typing import Annotated
import asyncio
import security
from security import oauth2_scheme, SECRET_KEY, ALGORITHM

import containers.responses as responses

router = fastapi.APIRouter()

try:
    client = Client()
except Exception as e:
    raise RuntimeError(f"Failed to connect to LXC: {e}")

@router.get("/status", response_model=responses.ContainerStatus)
async def container_status(token: Annotated[str, fastapi.Depends(oauth2_scheme)]):
    """Get the status of the current container"""
    ucinetid = security.verify_credentials(token) # Verify the credentials (An exception will occur if not valid)

    # Get the list of containers
    containers = await asyncio.to_thread(client.containers.all)

    for container in containers:
        if container.name == ucinetid:
            return responses.ContainerStatus(success=True, status=container.status)

    return responses.ContainerStatus(success=False, status=None)

@router.put("/start", response_model=responses.ContainerAction)
async def container_start(token: Annotated[str, Depends(oauth2_scheme)]):
    """Start the named container"""
    ucinetid = security.verify_credentials(token) # Verify the credentials (An exception will occur if not valid)

    containers = await asyncio.to_thread(client.containers.all)
    for container in containers:
        if container.name == ucinetid:
            try:
                await asyncio.to_thread(container.start)
                return responses.ContainerAction(success=True, message="Sent start request")
            except:
                return responses.ContainerAction(success=True, message="Something went wrong")

    return responses.ContainerAction(success=False, message="Server not found")

@router.put("/stop", response_model=responses.ContainerAction)
async def container_stop(token: Annotated[str, fastapi.Depends(oauth2_scheme)]):
    """Stop the named container"""
    ucinetid = security.verify_credentials(token) # Verify the credentials (An exception will occur if not valid)

    containers = await asyncio.to_thread(client.containers.all)
    for container in containers:
        if container.name == ucinetid:
            try:
                await asyncio.to_thread(container.stop)
                return responses.ContainerAction(success=True, message="Sent stop request")
            except:
                return responses.ContainerAction(success=False, message="Something went wrong")

    return responses.ContainerAction(success=False, message="Server not found")

@router.put("/restart", response_model=responses.ContainerAction)
async def container_restart(token: Annotated[str, fastapi.Depends(oauth2_scheme)]):
    """Restart the named container"""
    ucinetid = security.verify_credentials(token) # Verify the credentials (An exception will occur if not valid)

    containers = await asyncio.to_thread(client.containers.all)
    for container in containers:
        if container.name == ucinetid:
            try:
                await asyncio.to_thread(container.restart)
                return responses.ContainerAction(success=True, message="Sent restart request")
            except:
                return responses.ContainerAction(success=False, message="Something went wrong")

    return responses.ContainerAction(success=False, message="Server not found")