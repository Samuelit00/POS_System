from sqlalchemy.orm import Session
from .. import models, schemas
from ..utils.security import hash_password, verify_password

def create_user(db: Session, user: schemas.UsuarioCreate):
    hashed = hash_password(user.password)
    db_user = models.Usuario(nombre=user.nombre, 
                             email=user.email, 
                             password_hash=hashed, 
                             rol=user.rol)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def get_user(db: Session, user_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == user_id).first()

def list_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Usuario).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user: schemas.UsuarioUpdate):
    db_user = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()
    if not db_user:
        return None
    
    update_data = user.model_dump(exclude_unset=True)
    
    # Hash password if provided
    if 'password' in update_data:
        update_data['password_hash'] = hash_password(update_data.pop('password'))
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):  
    user = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()  
    if user:  
        db.delete(user)  
        db.commit()  
    return user