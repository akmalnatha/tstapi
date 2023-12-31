from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from db.connection import connectDB
from routes.jwt import get_current_user, check_is_login
from api.url import holiday_recomendation
import requests

ayokebali = APIRouter(tags=["HOLIDAY"])

@ayokebali.get('/destination')
async def read_data(current_user: Annotated[dict, Depends(get_current_user)]):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = current_user['holiday_token']
    if token:
        friend_service_url = holiday_recomendation
        destination_url = f"{friend_service_url}/destination"
        headers = {
            'accept': 'application/json',
            "Authorization": f"Bearer {token}"
        }

        try:
            # Kirim permintaan GET ke layanan teman
            response = requests.get(destination_url, headers=headers)
            response.raise_for_status()
            destination_data = response.json()
            return {
                "code": 200,
                "messages" : "Get All Destination successfully",
                "data" : destination_data
                }
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Failed to get destination data from holiday's service: {str(e)}")
    else:
        return {
                "code": 404,
                "messages" : "Failed get All Destination"
                }

@ayokebali.get('/destination/{id}')
async def read_data_by_id(id: int,current_user: Annotated[dict, Depends(get_current_user)]):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = current_user['holiday_token']
    if token:
        friend_service_url = holiday_recomendation
        destination_url = f"{friend_service_url}/destination/{id}"
        headers = {
            'accept': 'application/json',
            "Authorization": f"Bearer {token}"
        }

        try:
            # Kirim permintaan GET ke layanan teman
            response = requests.get(destination_url, headers=headers)
            response.raise_for_status()
            destination_data = response.json()
            return {
                "code": 200,
                "messages" : "Get Destination successfully",
                "data" : destination_data
                }
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Failed to get destination data from friend's service: {str(e)}")
    else:
        return {
                "code": 404,
                "messages" : "Failed get Destination Data"
                }