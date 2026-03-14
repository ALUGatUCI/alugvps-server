#! /usr/bin/env python3

import pathlib
import sqlmodel
import sys
from database.models import Request

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
                print(f"ID: {request.id}\nBody: {request.request}", end="\n\n")