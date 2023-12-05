import uvicorn
from fastapi import FastAPI

from routes.kereta import kereta
from routes.tiket import tiket
from routes.auth import auth
from routes.holiday_recomendation import ayokebali
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(kereta)
app.include_router(tiket)
app.include_router(auth)
app.include_router(ayokebali)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)