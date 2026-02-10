import os
import json
import pathlib
import subprocess

def _create_config_file():
    """Guided process for creating the program configuration file"""

    config_dir = pathlib.Path.home() / ".alugvps-server"
    config_file = pathlib.Path.home() / ".alugvps-server" / "config.json"

    # Skip file creation if it already exists
    if config_file.exists():
        return

    config = {
        "secret_key": None, # Secret key for jwt encoding (run openssl rand -hex 32)
        "port": None, # Port the API will listen to
        "acc_limit": None, # Limit the number of LXC container instances on this machine
        "cpu_limit": None, # Limit CPU resources for newly created containers
        "ram_limit": None, # Limit RAM resources for newly created containers
        "disk_limit": None # Limit the amount of storage for newly created containers
    }

    # Begin the guided setup process
    print("No configuration file detected, so start the guided setup process...")

    # Start by creating the secret key
    config["secret_key"] = subprocess.run(["openssl", "rand", "-hex", "32"], capture_output=True, text=True).stdout.strip()
    print("Successfully created a secret key")

    # Ask for a port number
    while True:
        try:
            port = int(input("Enter a port number (IPv4): "))
        except:
            print("Please enter a valid integer")
            continue

        if port < 0 or port > 65535:
            print("Please enter a valid port number")
            continue
        else:
            config["port"] = port
            break

    # Get the account limit
    while True:
        limit = input("Enter a limit for the number of accounts on this server (or leave blank to disable): ")
        if limit == "":
            break
        else:
            try:
                limit = int(limit)

                if limit < 1:
                    print("Please enter a valid limit")
                    continue

                config["acc_limit"] = limit
                break
            except:
                print("Please enter a valid integer")
                continue

    # Get the CPU limit for containers
    while True:
        try:
            limit = int(input("Enter the CPU core limit for containers: "))

            if limit < 1:
                print("Please enter a valid limit")
                continue

            config["cpu_limit"] = limit
            break
        except:
            print("Please enter a valid integer")
            continue

    # Get the RAM limit for containers
    while True:
        try:
            limit = int(input("Enter the RAM limit (in GiBs) for containers: "))

            if limit < 1:
                print("Please enter a valid limit")
                continue

            config["ram_limit"] = limit
            break
        except:
            print("Please enter a valid integer")
            continue

    # Get the storage limit for containers (in GiBs)
    while True:
        try:
            limit = int(input("Enter the disk limit (in GiBs) for containers: "))

            if limit < 10: # At least 10 for containers to install most distros
                print("Please enter a valid limit")
                continue

            config["disk_limit"] = limit
            break
        except:
            print("Please enter a valid integer")
            continue

    if not config_dir.exists():
        os.mkdir(config_dir)

    with open(config_file, "w") as f: # Create the config file
        json.dump(config, f, indent=4)

    print("Successfully created the configuration file")

def read_config_file(key: str):
    _create_config_file()

    config_file = json.load(open(pathlib.Path.home() / ".alugvps-server" / "config.json"))

    return config_file[key]