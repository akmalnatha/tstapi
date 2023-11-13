from datetime import timedelta
import os
import typing
from fastapi import APIRouter, Depends, Form, HTTPException, status
from routes.jwt import create_access_token, get_current_user, check_is_admin
from passlib.context import CryptContext
from db.connection import cursor, conn
from models.token import Token
from models.user import User

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = int(60)

auth = APIRouter()

# Token endpoint
@auth.post("/login", response_model=Token)
async def login_for_access_token(username: str = Form(...), password: str = Form(...)):
    query = ("SELECT * FROM user WHERE username = %s")
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    if result and pwd_context.verify(password, result["password"]):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )
        return {"message": "Login successfully", "access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Registration endpoint
@auth.post("/register")
async def register(username: str = Form(...), nama: str = Form(...), email: str = Form(...), password: str = Form(...), role: str = Form(...)):
    # Check sudah ada belum
    query = ("SELECT * FROM user WHERE username = %s")
    cursor.execute(query, (username,))
    result = cursor.fetchall()
    if result:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Username already exist")
    
    query = ("SELECT * FROM user WHERE email = %s")
    cursor.execute(query, (email,))
    result = cursor.fetchall()
    if result:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Email already exist")
    
    hashed_password = pwd_context.hash(password)
    query = "INSERT INTO user (username, nama, email, password, role) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (username, nama, email, hashed_password, role,))
    conn.commit()
    return {
            "code": 200,
            "messages" : "Register successfully",
            "data" : {
                "fullname" : nama,
                "username" : username,
                "email" : email,
            }
    }

# Protected endpoint
@auth.get("/user/me")
async def read_user_me(current_user: typing.Annotated[User, Depends(get_current_user)]):
    return current_user

@auth.get('/user')
async def read_data_all(check: typing.Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    query = "SELECT * FROM user;"
    cursor.execute(query)
    data = cursor.fetchall()
    return {
        "code": 200,
        "messages" : "Get All user successfully",
        "data" : data
    }

@auth.get('/user/{id}')
async def read_data_by_id(id: int, check: typing.Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    select_query = "SELECT * FROM user WHERE id = %s;"
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data user: {id} Not Found")

    return {
        "code": 200,
        "messages" : "Get user successfully",
        "data" : data
    }
    
@auth.post('/user')
async def write_data_by_admin(user: User, check: typing.Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    user_json = user.model_dump()
    query = "INSERT INTO user(username, nama, email, password, role) VALUES(%s,%s,%s,%s,%s);"
    cursor.execute(query, (user_json["username"], user_json["nama"], user_json["email"], user_json["password"], user_json["role"],))
    conn.commit()

    select_query = "SELECT * FROM user WHERE id = LAST_INSERT_ID();"
    cursor.execute(select_query)
    new_user = cursor.fetchone()

    return {
        "code": 200,
        "messages" : "Add user successfully",
        "data" : new_user
    }
    
@auth.put('/user/{id}')
async def update_data(user: User, id:int, check: typing.Annotated[User, Depends(get_current_user)]):
    if check["id"] != id and check["role"] != "admin":
        return
    user_json = user.model_dump()
    select_query = "SELECT * FROM user WHERE id = %s;"
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data user id {id} Not Found")
    
    query = "UPDATE user SET username=%s, nama=%s, email=%s, role=%s WHERE user.id = %s;"
    cursor.execute(query, (user_json["username"], user_json["nama"], user_json["email"], user_json["role"], id,))
    conn.commit()

    select_query = "SELECT * FROM user WHERE user.id = %s;"
    cursor.execute(select_query, (id,))
    new_user = cursor.fetchone()
    
    return {
        "code": 200,
        "messages" : "Update user successfully",
        "data" : new_user
    }

@auth.delete('/user/{id}')
async def delete_data(id: int, check: typing.Annotated[bool, Depends(check_is_admin)]):
    if not check:
        return
    select_query = "SELECT * FROM user WHERE id = %s;"
    cursor.execute(select_query, (id,))
    data = cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data user id {id} Not Found")
    
    query = "DELETE FROM user WHERE id = %s;"
    cursor.execute(query, (id,))
    conn.commit()
    return {
        "code": 200,
        "messages" : "Delete user successfully",
    }