from sqlalchemy.orm import Session
from sqlalchemy import desc
from .. import models, schemas
from decimal import Decimal
from typing import Optional
from datetime import datetime, date

def create_sale(db: Session, sale: schemas.VentaCreate, usuario_id: int):
    # Transactional flow handled by caller if desired (Session used inline here)
    total = Decimal('0.00')
    # Lock products while checking stock
    items = []
    for item in sale.detalles:
        producto_id = item['producto_id']
        cantidad = item['cantidad']
        precio_unitario = Decimal(str(item['precio_unitario']))
        
        prod = db.query(models.Producto).filter(models.Producto.id == producto_id).with_for_update().first()
        if not prod:
            raise ValueError(f'Producto {producto_id} no existe')
        if prod.stock < cantidad:
            raise ValueError(f'Stock insuficiente para producto {prod.nombre}')
        
        subtotal = precio_unitario * cantidad
        total += subtotal
        items.append((prod, cantidad, precio_unitario, subtotal))
    
    # Create sale
    db_sale = models.Venta(usuario_id=usuario_id, total=total, metodo_pago=sale.metodo_pago)
    db.add(db_sale)
    db.flush()  # get id
    
    # Create detail rows and update stock
    for prod, cantidad, precio_unitario, subtotal in items:
        detail = models.DetalleVenta(
            venta_id=db_sale.id, 
            producto_id=prod.id, 
            cantidad=cantidad, 
            precio_unitario=precio_unitario, 
            subtotal=subtotal
        )
        db.add(detail)
        prod.stock = prod.stock - cantidad
    
    db.commit()
    db.refresh(db_sale)
    return db_sale

def get_sale(db: Session, sale_id: int):  
    return db.query(models.Venta).filter(models.Venta.id == sale_id).first()  

def get_sale_with_details(db: Session, sale_id: int):
    sale = db.query(models.Venta).filter(models.Venta.id == sale_id).first()
    if not sale:
        return None
    
    detalles = db.query(models.DetalleVenta).filter(models.DetalleVenta.venta_id == sale_id).all()
    
    detalles_out = []
    for detalle in detalles:
        producto = db.query(models.Producto).filter(models.Producto.id == detalle.producto_id).first()
        detalles_out.append(schemas.DetalleVentaOut(
            producto_id=detalle.producto_id,
            producto_nombre=producto.nombre if producto else "Producto no encontrado",
            cantidad=detalle.cantidad,
            precio_unitario=float(detalle.precio_unitario),
            subtotal=float(detalle.subtotal)
        ))
    
    usuario = db.query(models.Usuario).filter(models.Usuario.id == sale.usuario_id).first()
    
    return schemas.VentaDetailOut(
        id=sale.id,
        usuario_id=sale.usuario_id,
        usuario_nombre=usuario.nombre if usuario else "Usuario no encontrado",
        fecha_creacion=sale.fecha_creacion.isoformat(),
        total=float(sale.total),
        detalles=detalles_out
    )

def list_sales(db: Session, skip: int = 0, limit: int = 100, start_date: Optional[date] = None, end_date: Optional[date] = None):
    query = db.query(models.Venta)
    
    if start_date:
        query = query.filter(models.Venta.fecha_creacion >= start_date)
    if end_date:
        # Include the entire end_date day
        end_datetime = datetime.combine(end_date, datetime.max.time())
        query = query.filter(models.Venta.fecha_creacion <= end_datetime)
    
    sales = query.order_by(desc(models.Venta.fecha_creacion)).offset(skip).limit(limit).all()
    
    result = []
    for sale in sales:
        sale_detail = get_sale_with_details(db, sale.id)
        if sale_detail:
            result.append(sale_detail)
    
    return result
  
def delete_sale(db: Session, sale_id: int):  
    sale = db.query(models.Venta).filter(models.Venta.id == sale_id).first()  
    if sale:  
        db.delete(sale)  
        db.commit()  
    return sale