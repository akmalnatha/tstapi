from typing import Optional
from pydantic import BaseModel

class Kereta(BaseModel):
	merk: str
	tipe: str
	jml_gerbong: int