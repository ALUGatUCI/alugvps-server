#! /usr/bin/env python3

import pathlib
import sqlmodel
import sys
from database.models import Request
from database.containers import create_new_container

database_path = pathlib.Path.home() / ".alugvps-server" / "alugvps.db"
engine = sqlmodel.create_engine(f"sqlite:///{database_path}", connect_args={'check_same_thread': False})
sqlmodel.SQLModel.metadata.create_all(engine)
session = sqlmodel.Session(engine)

arguments = sys.argv

if __name__ == "__main__":
    if len(arguments) == 2:
        if arguments[1] == "list":
            requests = session.exec(sqlmodel.select(Request)).all()
            for request in requests:
                print(f"ID: {request.id}\nBody: {request.request}\n\n")
    if len(arguments) == 3:
        if arguments[1] == "delete":
            request = session.get(Request, int(arguments[2]))
            if request is not None:
                session.delete(request)
                session.commit()
                print(f"Deleted request with ID {arguments[2]}")
            else:
                print(f"No request found with ID {arguments[2]}")
        if arguments[1] == "view":
            request = session.get(Request, int(arguments[2]))
            if request is not None:
                print(f"ID: {request.id}\nBody: {request.request}\n\n")
            else:
                print(f"No request found with ID {arguments[2]}")
        if arguments[1] == "approve":
            request = session.get(Request, int(arguments[2]))
            if request is not None:
                # Create the container
                try:
                    create_new_container(request.id)
                except Exception as e:
                    print(f"Error creating container: {e}")
                    sys.exit(1)

                print(f"Approved request with ID {arguments[2]}")
                session.delete(request)
                session.commit()
            else:
                print(f"No request found with ID {arguments[2]}")