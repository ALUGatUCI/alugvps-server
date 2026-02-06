import sqlmodel

engine = sqlmodel.create_engine('sqlite:///accounts.db', connect_args={'check_same_thread': False})
session = None

def create_db_and_tables():
    global session

    sqlmodel.SQLModel.metadata.create_all(engine)
    session = sqlmodel.Session(engine)
