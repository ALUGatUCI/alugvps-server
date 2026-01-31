from fastapi import FastAPI
import uvicorn
from containers import router as containers
from accounts import router as accounts
from database import database

app = FastAPI()

@app.on_event("startup")
def on_startup():
    database.create_db_and_tables()

# app.include_router(containers, prefix="/containers")
app.include_router(accounts, prefix="/accounts")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)