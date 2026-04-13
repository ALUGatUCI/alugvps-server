#! /usr/bin/env python3

import pathlib
import sqlmodel
from sqlmodel import select, func
import sys
import asyncio
from database.models import Request, Account
from database.containers import create_new_container
from configuration import configuration

# Create the database engine and session
database_path = pathlib.Path.home() / ".alugvps-server" / "alugvps.db"
engine = sqlmodel.create_engine(f"sqlite:///{database_path}", connect_args={'check_same_thread': False})
sqlmodel.SQLModel.metadata.create_all(engine)
session = sqlmodel.Session(engine)

# Get the command line arguments
arguments = sys.argv

async def entry_point():
    if len(arguments) == 3:
        if arguments[1] == "view": # View a request with the given ID
            request = session.get(Request, int(arguments[2]))
            if request is not None:
                print(f"ID: {request.id}\nBody: {request.request}\n\n")
            else:
                print(f"No request found with ID {arguments[2]}")
        if arguments[1] == "approve": # Approve a request with the given ID
            # Check if there is anymore space for accounts
            if configuration.read_config_file("acc_limit") is not None:
                statement = select(func.count()).select_from(Account)
                result = session.execute(statement).one()[0]

                if result >= configuration.read_config_file("acc_limit"):
                    print("Account limit on server reached")
                    sys.exit(1)

            request = session.get(Request, int(arguments[2]))
            if request is not None:
                # Create the container
                try:
                    await create_new_container(request.id)
                except Exception as e:
                    print(f"Error creating container: {e}")
                    sys.exit(1)

                print(f"Approved request with ID {arguments[2]}")
                session.delete(request)
                session.commit()
            else:
                print(f"No request found with ID {arguments[2]}")
        if arguments[1] == "list": # List all requests or users
            if arguments[2] == "requests":
                requests = session.exec(sqlmodel.select(Request)).all()
                for request in requests:
                    print(f"ID: {request.id}\nBody: {request.request}\n\n")
            elif arguments[2] == "users":
                users = session.exec(sqlmodel.select(Account)).all()
                for user in users:
                    print(f"ID: {user.id}\nEmail: {user.email}\nBanned: {user.banned}\nConfirmed: {user.confirmed}\n\n")
            else:
                print(f"Unknown list type: {arguments[2]}")
        if arguments[1] == "ban": # Ban a user with the given ID
            user = session.get(Account, int(arguments[2]))
            if user is not None:
                user.banned = True
                session.commit()
                print(f"Banned user with ID {arguments[2]}")
            else:
                print(f"No user found with ID {arguments[2]}")
        if arguments[1] == "unban": # Unban a user with the given ID
            user = session.get(Account, int(arguments[2]))
            if user is not None:
                user.banned = False
                session.commit()
                print(f"Unbanned user with ID {arguments[2]}")
            else:
                print(f"No user found with ID {arguments[2]}")
    elif len(arguments) == 4:
        if arguments[1] == "delete": # Delete a request or user with the given ID
            if arguments[2] == "request":
                request = session.get(Request, int(arguments[3]))
                if request is not None:
                    session.delete(request)
                    session.commit()
                    print(f"Deleted request with ID {arguments[3]}")
                else:
                    print(f"No request found with ID {arguments[3]}")
            elif arguments[2] == "users":
                user = session.get(Account, int(arguments[3]))
                if user is not None:
                    session.delete(user)
                    session.commit()
                    print(f"Deleted user with ID {arguments[3]}")
                else:
                    print(f"No user found with ID {arguments[3]}")
            else:
                print(f"Unknown delete type: {arguments[2]}")
    else:
        print("Implement help later")

# Implement a simple CLI for managing requests and users
if __name__ == "__main__":
    asyncio.run(entry_point())
