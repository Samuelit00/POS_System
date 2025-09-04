
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix='/productos', tags=['productos'])

@router.post('/', response_model=schemas.ProductoOut)
def create_product(product: schemas.ProductoCreate, db: Session = Depends(get_db)):
    return crud.products.create_product(db, product)

@router.get('/', response_model=list[schemas.ProductoOut])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.products.list_products(db, skip, limit)

@router.get('/{product_id}', response_model=schemas.ProductoOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    prod = crud.products.get_product(db, product_id)
    if not prod:
        raise HTTPException(status_code=404, detail='Producto no encontrado')
    return prod
