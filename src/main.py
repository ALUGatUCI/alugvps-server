from fastapi import FastAPI, Depends
import uvicorn
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from accounts.accounts import login_to_account, router as accounts
from containers import router as containers
from configuration import configuration
from database import database
import sys
import os

app = FastAPI()

@app.on_event("startup")
def on_startup():
    database.create_db_and_tables()

@app.post("/token")
def login_with_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return login_to_account(form_data.username, form_data.password)

def _launch_app():
    app.include_router(containers, prefix="/containers")
    app.include_router(accounts, prefix="/accounts")

    uvicorn.run(app, host="0.0.0.0", port=configuration.read_config_file("port"))

if __name__ == "__main__":
    configuration.create_config_file() # Starts guided config creation if file doesn't exist

    _launch_app() # Main function

    sys.exit(0)