from http.client import HTTPException, HTTPResponse

import fastapi
from fastapi import Depends
from pylxd import Client
from typing import Annotated

from sqlmodel import select
from starlette import status

from security import oauth2_scheme
import database.database as database
from database.models import Container, Account
from containers.body import AddPort, RemovePort
import asyncio
import security

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

@router.post("/port/add", response_model=responses.ContainerAction)
async def add_port(token: Annotated[str, fastapi.Depends(oauth2_scheme)], new_forward: AddPort = Depends()):
    """Add forward port to the container"""

    ucinetid = security.verify_credentials(token) # Verify the credentials (An exception will occur if not valid)

    containers = await asyncio.to_thread(client.containers.all)
    for container in containers:
        if container.name == ucinetid:
            session = database.session

            # Start by getting the account info
            acc_statement = select(Account).where(Account.email == f"{ucinetid}@uci.edu")
            account = session.exec(acc_statement).first()

            # Now get the ID to get the associated container's info
            account_id = account.id
            cont_statement = select(Container).where(Container.id == account_id)
            container_data = session.exec(cont_statement).first()

            # Now validate that the given listening port is in the list
            if new_forward.listen not in container_data.forward_ports:
                raise fastapi.HTTPException(status_code=400, detail="An invalid port was specified")

            new_port_map = {
                "type": "proxy",
                "listen": f"tcp:0.0.0.0:{new_forward.listen}", # Port on the HOST
                "connect": f"tcp:127.0.0.1:{new_forward.connect}"  # Port inside the CONTAINER
            }

            container.devices[new_forward.name] = new_port_map

            container.save()

        return responses.ContainerAction(success=True, message="Sent forward port added")

@router.delete("/port/delete", response_model=responses.ContainerAction)
async def remove_port(token: Annotated[str, fastapi.Depends(oauth2_scheme)], remove: RemovePort = Depends()):
    """Removes a specified port"""
    ucinetid = security.verify_credentials(token) # Verify the credentials (An exception will occur if not valid)

    containers = await asyncio.to_thread(client.containers.all)
    for container in containers:
        if container.name == ucinetid:
            # Now check if the named port is in the devices dictioanary
            # BE SURE THEY CANNOT REMOVE 'ssh-forward' or 'root' TO PREVENT INACCESSIBILITY
            if (remove.name != "ssh-forward"
                and remove.name != "root"
                and remove.name in container.devices.keys()
            ):
                del container.devices[remove.name]
                container.save()

                return responses.ContainerAction(success=True, message="Sent delete request")
            else:
                return responses.ContainerAction(success=False, message="Named port is invalid")

@router.get("/port/list", response_model=responses.PortsList)
async def get_used_port_list(token: Annotated[str, fastapi.Depends(oauth2_scheme)]):
    """Retrieves a list of all used forwarding ports"""
    ucinetid = security.verify_credentials(token) # Verify the credentials (An exception will occur if not valid)

    containers = await asyncio.to_thread(client.containers.all)
    for container in containers:
        if container.name == ucinetid:
            used_ports = []

            for device in container.devices.items():
                if device[1]["type"] == "proxy" and device[0] != "ssh-forward":
                    used_ports.append(tuple(device))

            return responses.PortsList(success=True, ports=used_ports)