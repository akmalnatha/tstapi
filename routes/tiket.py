from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from db.connection import connectDB
from routes.jwt import check_is_admin, check_is_login, get_current_user
from models.tiket import Tiket
from models.user import User
from routes.kereta import read_data_by_id as read_data_by_idKereta

tiket = APIRouter(tags=["TIKET"])

@tiket.get('/tiket')
async def read_data(check: Annotated[bool, Depends(check_is_admin)]):
    conn = connectDB()
    cursor = conn.cursor(dictionary=True)
    if not check:
        return
    query = "SELECT * FROM tiket;"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return {
        "code": 200,
        "messages" : "Get All Tiket successfully",
        "data" : data
    }

@tiket.get('/tiket/{id}')
async def read_data_by_id(id: int, check: Annotated[bool, Depends(check_is_admin)]):
    conn = connectDB()
    cursor = conn.cursor(dictionary=True)
    if not check:
        return
    select_query = "SELECT * FROM tiket WHERE id = %s;"
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data Tiket: {id} Not Found")

    return {
        "code": 200,
        "messages" : "Get Tiket successfully",
        "data" : data
    }
    
@tiket.get('/tiket/user/{userId}')
async def read_data_by_userId(user_id: int, check: Annotated[bool, Depends(get_current_user)]):
    conn = connectDB()
    cursor = conn.cursor(dictionary=True)
    if check["id"] != user_id and check["role"] != "admin":
        return
    select_query = "SELECT * FROM tiket WHERE user_id = %s;"
    cursor.execute(select_query, (user_id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data Tiket: with user {id} Not Found")

    return {
        "code": 200,
        "messages" : "Get Tiket by User successfully",
        "data" : data
    }

@tiket.post('/tiket')
async def write_data(tiket: Tiket, check: Annotated[bool, Depends(check_is_login)], user: Annotated[User, Depends(get_current_user)]):
    conn = connectDB()
    cursor = conn.cursor(dictionary=True)
    if not check:
        return
    tiket_json = tiket.model_dump()
    
    await read_data_by_idKereta(tiket_json["kereta_id"]) 
    query = "INSERT INTO tiket(user_id, penumpang_id, kereta_id, date_time) VALUES(%s,%s,%s,%s);"
    cursor.execute(query, (user["id"], tiket_json["penumpang_id"], tiket_json["kereta_id"], tiket_json["date_time"]))
    conn.commit()

    select_query = "SELECT * FROM tiket WHERE id = LAST_INSERT_ID();"
    cursor.execute(select_query)
    new_tiket = cursor.fetchone()
    cursor.close()
    conn.close()

    return {
            "code": 200,
            "messages" : "Add Tiket successfully",
            "data" : new_tiket
    }
    
@tiket.put('/tiket/{id}')
async def update_data(tiket: Tiket, id:int, user: Annotated[User, Depends(get_current_user)]):
    conn = connectDB()
    cursor = conn.cursor(dictionary=True)
    check_user_query = "SELECT * FROM tiket WHERE id = %s;"
    cursor.execute(check_user_query, (id,))
    check_user = cursor.fetchone()
    if user["id"] != check_user["user_id"] and user["role"] != "admin":
        return
    tiket_json = tiket.model_dump()
    select_query = "SELECT * FROM tiket WHERE id = %s;"
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data Tiket id {id} Not Found")
    
    await read_data_by_idKereta(tiket_json["kereta_id"])
    query = "UPDATE tiket SET penumpang_id = %s, kereta_id = %s, date_time=%s, notes=%s WHERE tiket.id = %s;"
    cursor.execute(query, (tiket_json["penumpang_id"], tiket_json["kereta_id"], tiket_json["date_time"], tiket_json["notes"], id,))
    conn.commit()

    select_query = "SELECT * FROM tiket WHERE tiket.id = %s;"
    cursor.execute(select_query, (id,))
    new_tiket = cursor.fetchone()
    cursor.close()
    conn.close()
    return {
        "code": 200,
        "messages" : "Update tiket successfully",
        "data" : new_tiket
    }

@tiket.delete('/tiket/{id}')
async def delete_data(id: int, check: Annotated[bool, Depends(check_is_admin)]):
    conn = connectDB()
    cursor = conn.cursor(dictionary=True)
    if not check:
        return
    select_query = "SELECT * FROM tiket WHERE id = %s;"
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data tiket id {id} Not Found")
    
    query = "DELETE FROM tiket WHERE id = %s;"
    cursor.execute(query, (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {
        "code": 200,
        "messages" : "Delete tiket successfully",
    }