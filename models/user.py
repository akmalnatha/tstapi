from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
	username: str
	nama: str
	email: str
	password: str
	role: str
	holiday_token: str