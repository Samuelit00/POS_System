from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix='/ventas', tags=['ventas'])

@router.post('/', response_model=schemas.VentaOut)
def create_sale(sale: schemas.VentaCreate, db: Session = Depends(get_db)):
    try:
        db_sale = crud.sales.create_sale(db, sale)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_sale
