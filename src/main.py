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

    uvicorn.run(app, host="0.0.0.0", port=configuration.config_file["port"])

if __name__ == "__main__":
    # The program must run as root to run due to UFW
    if os.getuid() != 0:
        print("You must be running as root for this program to function")
        sys.exit(1)

    if not configuration.config_file_exists(): # Create the config file if it doesn't exist
        configuration.create_config_file()

    configuration.load_config_file() # Load the config file into memory

    _launch_app()

    sys.exit(0)