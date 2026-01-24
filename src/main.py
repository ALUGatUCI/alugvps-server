from fastapi import FastAPI, HTTPException, Query
from pylxd import Client
import uvicorn
import asyncio
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()
client = Client()

@app.get("/containers/list")
async def containers_list():
    containers = await asyncio.to_thread(client.containers.all)
    return containers

@app.get("/containers/{name}/status")
async def container_status(name: str):
    # Get the list of containers
    containers = await asyncio.to_thread(client.containers.all)

    for container in containers:
        if container.name == name:
            return container.status

    return HTTPException(status_code=404, detail="Container not found")

@app.get("/containers/{name}/start")
async def container_start(name: str):
    containers = await asyncio.to_thread(client.containers.all)
    for container in containers:
        if container.name == name:
            try:
                await asyncio.to_thread(container.start)
                return HTTPException(status_code=200, detail="Container started")
            except Exception as e:
                return HTTPException(status_code=500, detail=str(e))

    return HTTPException(status_code=404, detail="Container not found")

@app.get("/containers/{name}/stop")
async def container_stop(name: str):
    containers = await asyncio.to_thread(client.containers.all)
    for container in containers:
        if container.name == name:
            try:
                await asyncio.to_thread(container.stop)
                return HTTPException(status_code=200, detail="Container stopped")
            except Exception as e:
                return HTTPException(status_code=500, detail=str(e))

    return HTTPException(status_code=404, detail="Container not found")

async def container_restart(name: str):
    containers = await asyncio.to_thread(client.containers.all)
    for container in containers:
        if container.name == name:
            try:
                await asyncio.to_thread(container.restart)
                return HTTPException(status_code=200, detail="Container restarted")
            except Exception as e:
                return HTTPException(status_code=500, detail=str(e))

    return HTTPException(status_code=404, detail="Container not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)