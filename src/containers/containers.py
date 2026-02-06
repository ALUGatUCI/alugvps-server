import fastapi
from pylxd import Client
from typing import Annotated
import asyncio
from security import oauth2_scheme

import containers.responses as responses

router = fastapi.APIRouter()

try:
    client = Client()
except Exception as e:
    raise RuntimeError(f"Failed to connect to LXC: {e}")

@router.get("/list", response_model=responses.ListContainers)
async def containers_list():
    """Get the list of containers in this server"""
    try:
        containers = await asyncio.to_thread(client.containers.all)

        containers = [container.name for container in containers]
    except:
        return responses.ListContainers(success=False, containers=None)

    return responses.ListContainers(success=True, containers=containers)


@router.get("/status/{name}", response_model=responses.ContainerStatus)
async def container_status(token: Annotated[str, fastapi.Depends(oauth2_scheme)], name: str):
    """Get the status of the current container"""
    # Get the list of containers
    containers = await asyncio.to_thread(client.containers.all)

    for container in containers:
        if container.name == name:
            return responses.ContainerStatus(success=True, status=container.status)

    return responses.ContainerStatus(success=False, status=None)

@router.put("/start/{name}", response_model=responses.ContainerStatus)
async def container_start(token: Annotated[str, fastapi.Depends(oauth2_scheme)], name: str):
    """Start the named container"""
    containers = await asyncio.to_thread(client.containers.all)
    for container in containers:
        if container.name == name:
            try:
                await asyncio.to_thread(container.start)
                return responses.ContainerAction(success=True, message="Sent start request")
            except:
                return responses.ContainerAction(success=True, message="Something went wrong")

    return responses.ContainerAction(success=False, message="Server not found")

@router.put("/stop/{name}", response_model=responses.ContainerStatus)
async def container_stop(token: Annotated[str, fastapi.Depends(oauth2_scheme)], name: str):
    """Stop the named container"""
    containers = await asyncio.to_thread(client.containers.all)
    for container in containers:
        if container.name == name:
            try:
                await asyncio.to_thread(container.stop)
                return {"success": True, "status": container.status}
            except:
                return {"success": False, "status": None}

    return {"success": False, "status": None}

@router.put("/restart/{name}")
async def container_restart(token: Annotated[str, fastapi.Depends(oauth2_scheme)], name: str):
    """Restart the named container"""
    containers = await asyncio.to_thread(client.containers.all)
    for container in containers:
        if container.name == name:
            try:
                await asyncio.to_thread(container.restart)
                return {"success": True, "status": container.status}
            except:
                return {"success": False, "status": None}

    return {"success": False, "status": None}