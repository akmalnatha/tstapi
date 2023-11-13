import uvicorn
from fastapi import FastAPI

from routes.kereta import kereta
from routes.tiket import tiket
from routes.user import user
from routes.auth import auth

app = FastAPI()

app.include_router(kereta)
app.include_router(tiket)
app.include_router(user)
app.include_router(auth)