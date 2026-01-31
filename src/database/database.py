from typing import Annotated
import sqlmodel
import fastapi

engine = sqlmodel.create_engine('sqlite:///accounts.db', connect_args={'check_same_thread': False})

def create_db_and_tables():
    sqlmodel.SQLModel.metadata.create_all(engine)

def get_session():
    with sqlmodel.Session(engine) as session:
        return session

SessionDep = Annotated[sqlmodel.Session, fastapi.Depends(get_session)]