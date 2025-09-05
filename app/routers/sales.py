from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db
from app.crud import sales
router = APIRouter(prefix='/ventas', tags=['ventas'])

@router.post('/', response_model=schemas.VentaOut)
def create_sale(sale: schemas.VentaCreate, db: Session = Depends(get_db)):
    try:
        db_sale = crud.sales.create_sale(db, sale)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_sale

@router.delete('/{sale_id}', status_code=204)  
def delete_sale(sale_id: int, db: Session = Depends(get_db)):  
    sale = crud.sales.get_sale(db, sale_id)  
    if not sale:  
        raise HTTPException(status_code=404, detail='Venta no encontrada')  
    crud.sales.delete_sale(db, sale_id)