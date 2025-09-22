
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud, models
from ..database import get_db
from app.crud import users
from ..utils.security import verify_password  
from ..utils.jwt import create_access_token
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

@router.put('/{user_id}', response_model=schemas.UsuarioOut)
def update_user(user_id: int, user: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    existing_user = crud.users.get_user(db, user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    return crud.users.update_user(db, user_id, user)

@router.post('/login')  
def login(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):  
    # Get user by email  
    user = crud.users.get_user_by_email(db, credentials.email)  
    if not user:  
        raise HTTPException(status_code=401, detail='Invalid credentials')  
      
    # Verify password  
    if not verify_password(credentials.password, user.password_hash):  
        raise HTTPException(status_code=401, detail='Invalid credentials')  
      
    # Create access token  
    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})  
      
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "nombre": user.nombre,
            "email": user.email,
            "rol": user.rol
        }
    }

@router.delete('/{user_id}', status_code=204)  
def delete_user(user_id: int, db: Session = Depends(get_db)):  
    user = crud.users.get_user(db, user_id)  
    if not user:  
        raise HTTPException(status_code=404, detail='Usuario no encontrado')  
    crud.users.delete_user(db, user_id)