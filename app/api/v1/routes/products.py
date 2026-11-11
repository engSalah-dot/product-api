from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import get_product_service
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product_service import ProductNotFoundError, ProductService

router = APIRouter(prefix="/products", tags=["products"])

ServiceDep = Annotated[ProductService, Depends(get_product_service)]


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(data: ProductCreate, service: ServiceDep) -> ProductRead:
    return service.create_product(data)


@router.get("", response_model=list[ProductRead])
async def list_products(
    service: ServiceDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
) -> list[ProductRead]:
    return service.list(skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, service: ServiceDep) -> ProductRead:
    try:
        return service.get_product(product_id)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: int, data: ProductUpdate, service: ServiceDep
) -> ProductRead:
    try:
        return service.update_product(product_id, data)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, service: ServiceDep) -> None:
    try:
        service.delete_product(product_id)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))