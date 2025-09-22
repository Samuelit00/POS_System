from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, date
from .. import schemas, crud, models
from ..database import get_db
from app.crud import sales
from ..utils.jwt import verify_token

router = APIRouter(prefix='/ventas', tags=['ventas'])

@router.post('/', response_model=schemas.VentaDetailOut)
def create_sale(
    sale: schemas.VentaCreate, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(verify_token)
):
    try:
        db_sale = crud.sales.create_sale(db, sale, current_user_id)
        return crud.sales.get_sale_with_details(db, db_sale.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get('/', response_model=list[schemas.VentaDetailOut])
def list_sales(
    skip: int = 0, 
    limit: int = 100, 
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    return crud.sales.list_sales(db, skip, limit, start_date, end_date)

@router.get('/{sale_id}', response_model=schemas.VentaDetailOut)
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = crud.sales.get_sale_with_details(db, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail='Venta no encontrada')
    return sale

@router.delete('/{sale_id}', status_code=204)  
def delete_sale(sale_id: int, db: Session = Depends(get_db)):  
    sale = crud.sales.get_sale(db, sale_id)  
    if not sale:  
        raise HTTPException(status_code=404, detail='Venta no encontrada')  
    crud.sales.delete_sale(db, sale_id)