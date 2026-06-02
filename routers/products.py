from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from repositories.schemas import ProductDB, ProductBase
from repositories.product_repository import ProductRepository
from services.auth_service import verify_token

router = APIRouter()

@router.get("/", response_model=List[ProductDB])
async def get_products(current_user: dict = Depends(verify_token)):
    return await ProductRepository.get_all_products()

@router.post("/", response_model=ProductDB, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductBase, current_user: dict = Depends(verify_token)):
    return await ProductRepository.create_product(product)

@router.put("/{id}", response_model=ProductDB)
async def update_product(id: str, product: ProductBase, current_user: dict = Depends(verify_token)):
    updated = await ProductRepository.update_product(id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return updated

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: str, current_user: dict = Depends(verify_token)):
    deleted = await ProductRepository.delete_product(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return None