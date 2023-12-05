from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from db.connection import connectDB
from routes.jwt import check_is_admin, check_is_login
from models.kereta import Kereta

kereta = APIRouter(tags=["KERETA"])

# @kereta.get('/kereta')
# async def read_data():
#     query = "SELECT * FROM kereta;"
#     cursor.execute(query)
#     data = cursor.fetchall()
#     return {
#         "code": 200,
#         "messages" : "Get All Kereta successfully",
#         "data" : data
#     }
    
@kereta.get('/kereta')
async def read_data_by_parameters(tujuan: str = None, keberangkatan: str = None, merk: str = None, tipe: str = None):
    conn = connectDB()
    cursor = conn.cursor(dictionary=True)
    conditions = []
    values = []

    if tujuan:
        conditions.append("LOWER(tujuan) = LOWER(%s)")
        values.append(tujuan.lower())
    if keberangkatan:
        conditions.append("LOWER(keberangkatan) = LOWER(%s)")
        values.append(keberangkatan.lower())
    if merk:
        conditions.append("LOWER(merk) = LOWER(%s)")
        values.append(merk.lower())
    if tipe:
        conditions.append("LOWER(tipe) = LOWER(%s)")
        values.append(tipe.lower())

    if not conditions:
        # If no parameters are provided, fetch all data
        query = "SELECT * FROM kereta;"
        cursor.execute(query)
        data = cursor.fetchall()
    else:
        where_clause = " AND ".join(conditions)
        select_query = f"SELECT * FROM kereta WHERE {where_clause};"
        cursor.execute(select_query, tuple(values))
        data = cursor.fetchall() 
    cursor.close()
    conn.close()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data Kereta Not Found")

    return {
        "code": 200,
        "messages": "Get Kereta successfully",
        "data": data
    }

@kereta.get('/kereta/{id}')
async def read_data_by_id(id: int):
    conn = connectDB()
    cursor = conn.cursor(dictionary=True)
    select_query = "SELECT * FROM kereta WHERE id = %s;"
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data Kereta: {id} Not Found")

    return {
        "code": 200,
        "messages" : "Get Kereta successfully",
        "data" : data
    }
    
# @kereta.get('/kereta/{tujuan}')
# async def read_data_by_tujuan(tujuan: str):
#     select_query = "SELECT * FROM kereta WHERE tujuan = %s;"
#     cursor.execute(select_query, (tujuan,))
#     data = cursor.fetchone()
#     if data is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data Kereta: {tujuan} Not Found")

#     return {
#         "code": 200,
#         "messages" : "Get Kereta successfully",
#         "data" : data
#     }
    
# @kereta.get('/kereta/{keberangkatan}')
# async def read_data_by_keberangkatan(keberangkatan: str):
#     select_query = "SELECT * FROM kereta WHERE keberangkatan = %s;"
#     cursor.execute(select_query, (keberangkatan,))
#     data = cursor.fetchone()
#     if data is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data Kereta: {keberangkatan} Not Found")

#     return {
#         "code": 200,
#         "messages" : "Get Kereta successfully",
#         "data" : data
#     }

@kereta.post('/kereta')
async def write_data(kereta: Kereta, check: Annotated[bool, Depends(check_is_admin)]):
    conn = connectDB()
    cursor = conn.cursor(dictionary=True)
    if not check:
        return
    kereta_json = kereta.model_dump()
    query = "INSERT INTO kereta(merk, tipe, jml_gerbong, keberangkatan, tujuan) VALUES(%s,%s,%s,%s,%s);"
    cursor.execute(query, (kereta_json["merk"], kereta_json["tipe"], kereta_json["jml_gerbong"], kereta_json["keberangkatan"], kereta_json["tujuan"]))
    conn.commit()

    select_query = "SELECT * FROM kereta WHERE id = LAST_INSERT_ID();"
    cursor.execute(select_query)
    new_kereta = cursor.fetchone()
    cursor.close()
    conn.close()

    return {
        "code": 200,
        "messages" : "Add Kereta successfully",
        "data" : new_kereta
    }
    
@kereta.put('/kereta/{id}')
async def update_data(kereta: Kereta, id:int, check: Annotated[bool, Depends(check_is_admin)]):
    conn = connectDB()
    cursor = conn.cursor(dictionary=True)
    if not check:
        return
    kereta_json = kereta.model_dump()
    select_query = "SELECT * FROM kereta WHERE id = %s;"
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data kereta id {id} Not Found")
    
    query = "UPDATE kereta SET merk=%s, tipe=%s, jml_gerbong=%s, keberangkatan=%s, tujuan=%s WHERE kereta.id = %s;"
    cursor.execute(query, (kereta_json["merk"], kereta_json["tipe"], kereta_json["jml_gerbong"], kereta_json["keberangkatan"], kereta_json["tujuan"], id,))
    conn.commit()

    select_query = "SELECT * FROM kereta WHERE kereta.id = %s;"
    cursor.execute(select_query, (id,))
    new_kereta = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return {
        "code": 200,
        "messages" : "Update kereta successfully",
        "data" : new_kereta
    }

@kereta.delete('/kereta/{id}')
async def delete_data(id: int, check: Annotated[bool, Depends(check_is_admin)]):
    conn = connectDB()
    cursor = conn.cursor(dictionary=True)
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
    cursor.close()
    conn.close()
    return {
        "code": 200,
        "messages" : "Delete kereta successfully",
    }