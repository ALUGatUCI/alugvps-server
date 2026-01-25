from fastapi import APIRouter, HTTPException
from pylxd import Client
import asyncio

import responses

router = APIRouter()
client = Client()

@router.get("/list", response_model=responses.ListContainers)
async def containers_list():
    try:
        containers = await asyncio.to_thread(client.containers.all)
    except:
        return {"success": False, "list": None}

    return {"success": True, "list": containers}


@router.get("/status/{name}", response_model=responses.ContainerStatus)
async def container_status(name: str):
    # Get the list of containers
    containers = await asyncio.to_thread(client.containers.all)

    for container in containers:
        if container.name == name:
            return {"success": True, "status": container.status}

    return {"success": False, "status": None}

@router.put("/start/{name}", response_model=responses.ContainerStatus)
async def container_start(name: str):
    containers = await asyncio.to_thread(client.containers.all)
    for container in containers:
        if container.name == name:
            try:
                await asyncio.to_thread(container.start)
                return {"success": True, "status": container.status}
            except:
                return {"success": False, "status": None}

    return {"success": False, "status": None}

@router.put("/stop/{name}", response_model=responses.ContainerStatus)
async def container_stop(name: str):
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
async def container_restart(name: str):
    containers = await asyncio.to_thread(client.containers.all)
    for container in containers:
        if container.name == name:
            try:
                await asyncio.to_thread(container.restart)
                return {"success": True, "status": container.status}
            except:
                return {"success": False, "status": None}

    return {"success": False, "status": None}