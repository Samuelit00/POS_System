from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base



"""
Pydantic
Aqui se encuentran todos las tablas de la base de datos montada en 
Postgresql, se hace uso de sqlalchemy para la definicion de los modelos
y mantener la integridad de los datos en un solo lenguaje, existen diferentes
tipos de relaciones que se pueden establecer entre las tablas.
"""
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False)  # admin | vendedor
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    ventas = relationship("Venta", back_populates="usuario")

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    precio = Column(Numeric(12,2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    detalles = relationship("DetalleVenta", back_populates="producto")

class Venta(Base):
    __tablename__ = "ventas"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    total = Column(Numeric(12,2), nullable=False)
    metodo_pago = Column(String(50), nullable=False, default="efectivo")

    usuario = relationship("Usuario", back_populates="ventas")
    items = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")

class DetalleVenta(Base):
    __tablename__ = "detalle_ventas"
    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(12,2), nullable=False)
    subtotal = Column(Numeric(12,2), nullable=False)

    venta = relationship("Venta", back_populates="items")
    producto = relationship("Producto", back_populates="detalles")
