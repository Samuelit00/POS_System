from sqlalchemy.orm import Session
from .. import models, schemas

def create_product(db: Session, product: schemas.ProductoCreate):
    db_prod = models.Producto(nombre=product.nombre, descripcion=product.descripcion, precio=product.precio, stock=product.stock)
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod

def get_product(db: Session, product_id: int):
    return db.query(models.Producto).filter(models.Producto.id == product_id).first()

def list_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Producto).offset(skip).limit(limit).all()

def update_stock(db: Session, product_id: int, delta: int):
    prod = db.query(models.Producto).filter(models.Producto.id == product_id).with_for_update().first()
    if prod is None:
        return None
    prod.stock = prod.stock + delta
    db.commit()
    db.refresh(prod)
    return prod
