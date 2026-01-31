from fastapi import FastAPI
import uvicorn
from containers import router as containers

app = FastAPI()

# app.include_router(containers, prefix="/containers")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)