import asyncio

from sqlalchemy import func
from sqlmodel import select

import configuration
from database.models import Account, AccountCreation
from database.models import Container
from database import database
from containers import client
from security.shacrypt512 import shacrypt


async def create_new_container(account_id: int, account: AccountCreation):
    """Creates a new container upon account creation"""

    # Calculate the SSH port forwarding number
    statement = select(func.count(Account.id))
    result = database.session.execute(statement).one()[0]

    new_container = Container(
        id = account_id,
        ssh_port = 10000 + (10 * result),
        forward_ports = [port for port in range(10000 + (10 * result) + 1, 10000 + (10 * result) + 10)]
    )

    # Add the container data to the table
    session = database.session

    session.add(new_container)
    session.commit()
    session.refresh(new_container)

    ucinetid = account.email[:account.email.find("@")]
    hashed_password = shacrypt(account.password.get_secret_value().encode('utf-8'))

    # Now create and start the actual container
    container_config = {
        "name": ucinetid,
        "type": "container",
        "ephemeral": False,
        "source": {
            "type": "image",
            "fingerprint": "ad33d28f277c" # Install Ubuntu 24.04
        },
        "config": {
            "limits.cpu": f"{configuration.read_config_file("cpu_limit")}",
            "limits.memory": f"{configuration.read_config_file("ram_limit")}GiB",
            "user.user-data": ("#cloud-config\n"
                              "ssh_pwauth: True\n"
                              "users:\n"
                              f"  - name: {ucinetid}\n"               # The username
                              "    sudo: ALL=(ALL) NOPASSWD:ALL\n" # Gives the user sudo rights
                              "    shell: /bin/bash\n"
                              "    lock_passwd: false\n"         # Crucial: allows password login
                              f"    passwd: {hashed_password}\n"   # Plain text password
                              "chpasswd:\n"
                              "  list: |\n"
                              f"    {ucinetid}:{hashed_password}\n"         # Redundant but ensures it sets
                              "  expire: False\n"
                              "runcmd:\n"
                              "  - systemctl enable --now ssh\n"
                               )
        },
        "devices": {
            "root": {
                "type": "disk",
                "path": "/",
                "pool": "default",
                "size": f"{configuration.read_config_file("disk_limit")}GiB"
            },
            # SSH Port Forwarding (Proxy Device)
            "ssh-forward": {
                "type": "proxy",
                "listen": f"tcp:0.0.0.0:{new_container.ssh_port}", # Port on the HOST
                "connect": "tcp:127.0.0.1:22"  # Port inside the CONTAINER
            }
        }
    }

    instance = await asyncio.to_thread(client.containers.create, container_config, wait=True)
    instance.start()