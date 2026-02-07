from fastapi import FastAPI, Depends
import uvicorn
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from accounts.accounts import login_to_account, router as accounts
from containers import router as containers
from database import database

app = FastAPI()

@app.on_event("startup")
def on_startup():
    database.create_db_and_tables()

app.include_router(containers, prefix="/containers")
app.include_router(accounts, prefix="/accounts")

@app.post("/token")
def login_with_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return login_to_account(form_data.username, form_data.password)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)