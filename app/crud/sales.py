from sqlalchemy.orm import Session
from .. import models, schemas
from decimal import Decimal

def create_sale(db: Session, sale: schemas.VentaCreate):
    # Transactional flow handled by caller if desired (Session used inline here)
    total = Decimal('0.00')
    # Lock products while checking stock
    items = []
    for item in sale.productos:
        prod = db.query(models.Producto).filter(models.Producto.id == item.producto_id).with_for_update().first()
        if not prod:
            raise ValueError(f'Producto {item.producto_id} no existe')
        if prod.stock < item.cantidad:
            raise ValueError(f'Stock insuficiente para producto {prod.nombre}')
        price = prod.precio
        subtotal = price * item.cantidad
        total += subtotal
        items.append((prod, item.cantidad, price, subtotal))
    # Create sale
    db_sale = models.Venta(usuario_id=sale.usuario_id, total=total)
    db.add(db_sale)
    db.flush()  # get id
    # Create detail rows and update stock
    for prod, cantidad, price, subtotal in items:
        detail = models.DetalleVenta(venta_id=db_sale.id, producto_id=prod.id, cantidad=cantidad, precio_unitario=price, subtotal=subtotal)
        db.add(detail)
        prod.stock = prod.stock - cantidad
    db.commit()
    db.refresh(db_sale)
    return db_sale
