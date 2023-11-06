from fastapi import FastAPI, HTTPException
import json
from pydantic import BaseModel

class Tiket(BaseModel):
	id: int
	user_id: int
	penumpang_id: int
	kereta_id: int

class User(BaseModel):
	id: int
	username: str
	nama: str
	verified: bool
	email: str
	password: str

class Kereta(BaseModel):
	id: int
	merk: str
	tipe: str
	jml_gerbong: int

json_filename="kai.json"

with open(json_filename,"r") as read_file:
	data = json.load(read_file)

app = FastAPI()

@app.get('/tiket')
async def getAllTiket():
	return data['tiket']


@app.get('/tiket/{tiket_id}')
async def getTiketById(tiket_id: int):
	for tiket_item in data['tiket']:
		if tiket_item['id'] == tiket_id:
			return tiket_item
	raise HTTPException(
		status_code=404, detail=f'Tiket not found'
	)

@app.get('/tiket/user/{userId}')
async def getTiketByUser(userId: int):
    idFound = False
    for user in data['user']:
        if(user['id'] == userId):
            idFound = True
    if idFound:
        tiketFound = False
        hasil = []
        for tiket in data['tiket']:
            if(tiket['user_id'] == userId):
                tiketFound = True
                hasil.append(tiket)
        if tiketFound:
            return hasil
        if not tiketFound:
            return "No tiket with the User ID"+str(userId)
    if not idFound: 
        raise HTTPException(
		status_code=404, detail=f'User ID not found'
	)

@app.post('/tiket')
async def addTiket(tiket: Tiket):
	tiket_dict = tiket.dict()
	tiket_found = False
	for tiket_item in data['tiket']:
		if tiket_item['id'] == tiket_dict['id']:
			tiket_found = True
			return "Tiket ID "+str(tiket_dict['id'])+" sudah digunakan."
	
	if not tiket_found:
		data['tiket'].append(tiket_dict)
		with open(json_filename,"w") as write_file:
			json.dump(data, write_file)

		return tiket_dict
	raise HTTPException(
		status_code=404, detail=f'Tiket not found'
	)

@app.put('/tiket')
async def updateTiket(tiket: Tiket):
	tiket_dict = tiket.dict()
	tiket_found = False
	for tiket_idx, tiket_item in enumerate(data['tiket']):
		if tiket_item['id'] == tiket_dict['id']:
			tiket_found = True
			data['tiket'][tiket_idx]=tiket_dict
			
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			return data['tiket']
	
	if not tiket_found:
		return "Tiket not found."
	raise HTTPException(
		status_code=404, detail=f'Tiket not found'
	)

@app.delete('/tiket/{tiket_id}')
async def deleteTiket(tiket_id: int):

	tiket_found = False
	for tiket_idx, tiket_item in enumerate(data['tiket']):
		if (tiket_item['id'] == tiket_id):
			tiket_found = True
			data['tiket'].pop(tiket_idx)
			
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			return "Data Deleted"
	
	if not tiket_found:
		return "tiket not found."
	raise HTTPException(
		status_code=404, detail=f'Tiket not found'
	)

@app.get('/kereta')
async def getAllKereta():
	return data['kereta']


@app.get('/kereta/{kereta_id}')
async def getKeretaById(kereta_id: int):
	for kereta_item in data['kereta']:
		if kereta_item['id'] == kereta_id:
			return kereta_item
	raise HTTPException(
		status_code=404, detail=f'Kereta not found'
	)

@app.post('/kereta')
async def addKereta(kereta: Kereta):
	kereta_dict = kereta.dict()
	kereta_found = False
	for kereta_item in data['kereta']:
		if kereta_item['id'] == kereta_dict['id']:
			kereta_found = True
			return "Kereta ID "+str(kereta_dict['id'])+" sudah digunakan."
	
	if not kereta_found:
		data['kereta'].append(kereta_dict)
		with open(json_filename,"w") as write_file:
			json.dump(data, write_file)

		return kereta_dict
	raise HTTPException(
		status_code=404, detail=f'Kereta not found'
	)

@app.put('/kereta')
async def updateKereta(kereta: Kereta):
	kereta_dict = kereta.dict()
	kereta_found = False
	for kereta_idx, kereta_item in enumerate(data['kereta']):
		if kereta_item['id'] == kereta_dict['id']:
			kereta_found = True
			data['kereta'][kereta_idx]=kereta_dict
			
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			return data['kereta']
	
	if not kereta_found:
		return "Kereta not found."
	raise HTTPException(
		status_code=404, detail=f'Kereta not found'
	)

@app.delete('/kereta/{kereta_id}')
async def deleteKereta(kereta_id: int):

	kereta_found = False
	for kereta_idx, kereta_item in enumerate(data['kereta']):
		if kereta_item['id'] == kereta_id:
			kereta_found = True
			data['kereta'].pop(kereta_idx)
			
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			return "Data Deleted"
	
	if not kereta_found:
		return "Kereta not found."
	raise HTTPException(
		status_code=404, detail=f'Kereta not found'
	)

@app.get('/user')
async def getAllKereta():
	return data['user']


@app.get('/user/{user_id}')
async def getUserById(user_id: int):
	for user_item in data['user']:
		if user_item['id'] == user_id:
			return user_item
	raise HTTPException(
		status_code=404, detail=f'User not found'
	)

@app.post('/user')
async def addUser(user: User):
	user_dict = user.dict()
	user_found = False
	for user_item in data['user']:
		if user_item['id'] == user_dict['id']:
			user_found = True
			return "User ID "+str(user_dict['id'])+" sudah digunakan."
	
	if not user_found:
		data['user'].append(user_dict)
		with open(json_filename,"w") as write_file:
			json.dump(data, write_file)

		return user_dict
	raise HTTPException(
		status_code=404, detail=f'User not found'
	)

@app.put('/user')
async def updateUser(user: User):
	user_dict = user.dict()
	user_found = False
	for user_idx, user_item in enumerate(data['user']):
		if user_item['id'] == user_dict['id']:
			user_found = True
			data['user'][user_idx]=user_dict
			
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			return data['user']
	
	if not user_found:
		return "User not found."
	raise HTTPException(
		status_code=404, detail=f'User not found'
	)

@app.delete('/user/{user_id}')
async def deleteUser(user_id: int):

	user_found = False
	for user_idx, user_item in enumerate(data['user']):
		if user_item['id'] == user_id:
			user_found = True
			data['user'].pop(user_idx)
			
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			return "Data Deleted"
	
	if not user_found:
		return "User not found."
	raise HTTPException(
		status_code=404, detail=f'User not found'
	)
