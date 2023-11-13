from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from db.connection import cursor, conn
from routes.jwt import check_is_admin
from models.kereta import Kereta

kereta = APIRouter()

@kereta.get('/kereta')
async def read_data(check: Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    query = "SELECT * FROM kereta;"
    cursor.execute(query)
    data = cursor.fetchall()
    return {
        "code": 200,
        "messages" : "Get All Kereta successfully",
        "data" : data
    }

@kereta.get('/kereta/{id}')
async def read_data(id: int, check: Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    select_query = "SELECT * FROM kereta WHERE id = %s;"
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data Kereta: {id} Not Found")

    return {
        "code": 200,
        "messages" : "Get Kereta successfully",
        "data" : data
    }

@kereta.post('/kereta')
async def write_data(kereta: Kereta, check: Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    kereta_json = kereta.model_dump()
    query = "INSERT INTO kereta(merk, tipe, jml_gerbong) VALUES(%s,%s,%s);"
    cursor.execute(query, (kereta_json["merk"], kereta_json["tipe"], kereta_json["jml_gerbong"]))
    conn.commit()

    select_query = "SELECT * FROM kereta WHERE id = LAST_INSERT_ID();"
    cursor.execute(select_query)
    new_kereta = cursor.fetchone()

    return {
        "code": 200,
        "messages" : "Add Kereta successfully",
        "data" : new_kereta
    }
    
@kereta.put('/kereta/{id}')
async def update_data(kereta: Kereta, id:int, check: Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    kereta_json = kereta.model_dump()
    select_query = "SELECT * FROM kereta WHERE id = %s;"
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data kereta id {id} Not Found")
    
    query = "UPDATE kereta SET merk=%s, tipe=%s, jml_gerbong=%s WHERE kereta.id = %s;"
    cursor.execute(query, (kereta_json["merk"], kereta_json["tipe"], kereta_json["jml_gerbong"], id,))
    conn.commit()

    select_query = "SELECT * FROM kereta WHERE kereta.id = %s;"
    cursor.execute(select_query, (id,))
    new_kereta = cursor.fetchone()
    
    return {
        "code": 200,
        "messages" : "Update kereta successfully",
        "data" : new_kereta
    }

@kereta.delete('/kereta/{id}')
async def delete_data(id: int, check: Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    select_query = "SELECT * FROM kereta WHERE id = %s;"
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data kereta id {id} Not Found")
    
    query = "DELETE FROM kereta WHERE id = %s;"
    cursor.execute(query, (id,))
    conn.commit()
    return {
        "code": 200,
        "messages" : "Delete kereta successfully",
    }