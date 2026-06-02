from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from repositories.schemas import UserDB, UserCreate
from repositories.user_repository import UserRepository
from services.auth_service import verify_token

router = APIRouter()

@router.get("/", response_model=List[UserDB])
async def get_all_users(current_user: dict = Depends(verify_token)):
    return await UserRepository.get_all_users()

@router.put("/{id}", response_model=UserDB)
async def update_user(id: str, user_data: UserCreate, current_user: dict = Depends(verify_token)):
    updated_user = await UserRepository.update_user(id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated_user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str, current_user: dict = Depends(verify_token)):
    deleted = await UserRepository.delete_user(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return None