from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from decimal import Decimal

"""
El objetivo de los esquemas es de definir la estructura de los 
datos que se recibirán y enviarán a través de la API.

Es un estandar de que nos permite validar información de nuestros modelos 
de datos.
"""

class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    rol: str  # 'admin' or 'vendedor'

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    rol: str

    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    rol: Optional[str] = None

class ProductoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float = Field(..., gt=0, description="Precio debe ser mayor a 0")
    stock: int = Field(..., ge=0, description="Stock debe ser mayor o igual a 0")

class ProductoOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    precio: float
    stock: int

    class Config:
        from_attributes = True

class DetalleVentaItem(BaseModel):
    producto_id: int
    cantidad: int = Field(..., gt=0, description="Cantidad debe ser mayor a 0")

class VentaCreate(BaseModel):
    metodo_pago: str
    detalles: List[dict]  # Will contain producto_id, cantidad, precio_unitario

class VentaOut(BaseModel):
    id: int
    usuario_id: int
    total: float

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):  
    email: EmailStr  
    password: str

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None

class DetalleVentaOut(BaseModel):
    producto_id: int
    producto_nombre: str
    cantidad: int
    precio_unitario: float
    subtotal: float

    class Config:
        from_attributes = True

class VentaDetailOut(BaseModel):
    id: int
    usuario_id: int
    usuario_nombre: str
    fecha_creacion: str
    total: float
    detalles: List[DetalleVentaOut]

    class Config:
        from_attributes = True

class ProductoTop(BaseModel):
    nombre: str
    cantidad: int
    total: float

class DashboardMetrics(BaseModel):
    total_ventas_hoy: float
    ventas_count_hoy: int
    productos_bajo_stock: int
    usuarios_activos: int
    productos_top: List[ProductoTop] = []