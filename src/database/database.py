import sqlmodel
import pathlib

path = pathlib.Path.home() / ".alugvps-server" / "alugvps.db"
engine = sqlmodel.create_engine(f"sqlite:///{path}", connect_args={'check_same_thread': False})
session = None

def create_db_and_tables():
    global session

    sqlmodel.SQLModel.metadata.create_all(engine)
    session = sqlmodel.Session(engine)
