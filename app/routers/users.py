
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud, models
from ..database import get_db
from app.crud import users
router = APIRouter(prefix='/usuarios', tags=['usuarios'])

@router.post('/', response_model=schemas.UsuarioOut)
def create_user(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    existing = crud.users.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')
    db_user = crud.users.create_user(db, user)
    return db_user

@router.get('/', response_model=list[schemas.UsuarioOut])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.users.list_users(db, skip, limit)

@router.get('/{user_id}', response_model=schemas.UsuarioOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    u = crud.users.get_user(db, user_id)
    if not u:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    return u
