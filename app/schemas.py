from pydantic import BaseModel, EmailStr, conint, condecimal
from typing import List, Optional

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
        orm_mode = True

class ProductoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: condecimal(max_digits=12, decimal_places=2)
    stock: conint(ge=0)

class ProductoOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    precio: float
    stock: int

    class Config:
        orm_mode = True

class DetalleVentaItem(BaseModel):
    producto_id: int
    cantidad: conint(gt=0)

class VentaCreate(BaseModel):
    usuario_id: int
    productos: List[DetalleVentaItem]

class VentaOut(BaseModel):
    id: int
    usuario_id: int
    total: float

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):  
    email: EmailStr  
    password: str