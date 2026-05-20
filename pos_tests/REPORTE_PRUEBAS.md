# Reporte de Pruebas Automatizadas — POS System
**Fecha de ejecución:** 2026-05-20  
**Ejecutado por:** Samuel Francisco Moncayo Moncayo  
**Servidor:** http://localhost:8000 (FastAPI + Uvicorn)  
**Framework de pruebas:** pytest 8.2.0 + requests 2.32.3  

---

## 1. Resumen Ejecutivo

| Métrica | Valor |
|---|---|
| Total de casos de prueba | 48 |
| Casos PASADOS | 43 |
| Casos FALLADOS | 5 |
| Tasa de éxito | 89.6 % |
| Duración total | ~2m 54s |
| Defectos encontrados | 5 (DEF-003 a DEF-007) |

---

## 2. Módulos Probados

| Módulo | Endpoint | Técnicas aplicadas | Casos |
|---|---|---|---|
| F1 — Login | POST /api/usuarios/login | Particiones de Equivalencia | 8 |
| F2 — Usuarios | POST /api/usuarios/ | PE + Valores Límite | 12 |
| F3 — Ventas | POST /api/ventas/ | PE + Valores Límite | 14 |
| F4 — Productos | POST /api/productos/ / GET /api/productos/ | PE + Valores Límite | 14 |

---

## 3. Resultados por Módulo

### F1 — Login de Usuarios (8/8 PASSED)

| ID | Descripción | Prioridad | Resultado |
|---|---|---|---|
| TC-L01 | Login con credenciales válidas → HTTP 200, retorna access_token | Alta | PASSED |
| TC-L02 | Email sin @ → HTTP 422 | Media | PASSED |
| TC-L03 | Email no registrado → HTTP 401, "Invalid credentials" | Alta | PASSED |
| TC-L04 | Password incorrecta → HTTP 401, "Invalid credentials" | Alta | PASSED |
| TC-L06 | Password vacía "" → HTTP 401 | Media | PASSED |
| TC-L07 | Campo email ausente → HTTP 422 | Baja | PASSED |
| TC-L08 | Campo password ausente → HTTP 422 | Baja | PASSED |
| TC-L09 | Email en MAYÚSCULAS → documenta si es case-sensitive | Media | PASSED |

**Observación TC-L09:** El sistema es case-sensitive con el email. `ADMIN@EXAMPLE.COM` fue rechazado con HTTP 401, lo que significa que los usuarios deben ingresar el email exactamente como fue registrado.

---

### F2 — Creación de Usuarios (10/12 PASSED)

| ID | Descripción | Prioridad | Resultado |
|---|---|---|---|
| TC-U01 | Usuario admin válido → HTTP 200, respuesta tiene id/nombre/email/rol | Alta | PASSED |
| TC-U02 | Usuario vendedor válido → HTTP 200, rol=vendedor | Alta | PASSED |
| TC-U03 | Nombre vacío "" → HTTP 422 | Media | **FAILED** |
| TC-U04 | Email sin @ → HTTP 422 | Media | PASSED |
| TC-U05 | Rol "supervisor" (inválido) → HTTP 422 o 500 | Alta | **FAILED** |
| TC-U06 | Campo nombre ausente → HTTP 422 | Media | PASSED |
| TC-U07 | Email duplicado → HTTP 400, "Email already registered" | Alta | PASSED |
| TC-U08 | Nombre de exactamente 100 chars → HTTP 200 | Baja | PASSED |
| TC-U09 | Nombre de 101 chars → HTTP 400/422/500 | Baja | PASSED |
| TC-U10 | Campo password ausente → HTTP 422 | Media | PASSED |
| TC-U11 | Password NO aparece en respuesta (seguridad) | Alta | PASSED |
| TC-U12 | Email en mayúsculas → documenta comportamiento | Media | PASSED |

**Observación TC-U11:** La contraseña no se devuelve en texto plano ni como hash bcrypt en la respuesta. La seguridad en este punto es correcta.  
**Observación TC-U09:** El sistema aceptó nombres de 101 caracteres (HTTP 200), lo que puede causar truncamiento silencioso en la base de datos (VARCHAR 100). No genera error explícito.

---

### F3 — Registro de Ventas (12/14 PASSED)

| ID | Descripción | Prioridad | Resultado |
|---|---|---|---|
| TC-V01 | Venta 1 producto → HTTP 200, total = precio × cantidad | Alta | PASSED |
| TC-V02 | Venta múltiples productos → HTTP 200, total = suma subtotales | Alta | PASSED |
| TC-V03 | Producto inexistente (id=999999) → HTTP 400 | Alta | PASSED |
| TC-V04 | Stock insuficiente (cantidad=999, stock=3) → HTTP 400 | Alta | PASSED |
| TC-V05 | Cantidad = 0 → HTTP 422 | Alta | **FAILED** |
| TC-V06 | Cantidad = -1 → HTTP 422 | Media | **FAILED** |
| TC-V07 | Cantidad = 1 (límite inferior válido) → HTTP 200 | Media | PASSED |
| TC-V08 | Cantidad = stock exacto → HTTP 200, stock queda en 0 | Alta | PASSED |
| TC-V09 | Cantidad = stock + 1 → HTTP 400 | Alta | PASSED |
| TC-V10 | Lista productos vacía [] → documenta resultado | Media | PASSED |
| TC-V11 | Cálculo total (100×3)+(250×2) = 800.00 | Alta | PASSED |
| TC-V12 | Stock se descuenta post-venta | Alta | PASSED |
| TC-V13 | Token con usuario_id inexistente → rechazo | Media | PASSED |
| TC-V14 | Precio decimal 99.99 × 2 = 199.98 | Alta | PASSED |

**Observación TC-V10:** Lista vacía retornó HTTP 200 con `total=0.0`. El sistema permite registrar ventas sin productos.  
**Observación TC-V13:** Token JWT con firma inválida fue correctamente rechazado con HTTP 401.

---

### F4 — Gestión de Productos (13/14 PASSED)

| ID | Descripción | Prioridad | Resultado |
|---|---|---|---|
| TC-P01 | Producto completo válido → HTTP 200, tiene id/nombre/precio/stock | Alta | PASSED |
| TC-P02 | Campo nombre ausente → HTTP 422 | Alta | PASSED |
| TC-P03 | Nombre vacío "" → HTTP 400/422 | Alta | **FAILED** |
| TC-P04 | Sin descripcion (opcional) → HTTP 200, descripcion=null | Alta | PASSED |
| TC-P05 | Precio = 0 → HTTP 422 | Alta | PASSED |
| TC-P06 | Precio = -100 → HTTP 422 | Alta | PASSED |
| TC-P07 | Precio = 0.01 (mínimo válido) → HTTP 200 | Media | PASSED |
| TC-P08 | Stock = 0 (límite inferior válido) → HTTP 200 | Media | PASSED |
| TC-P09 | Stock = -1 → HTTP 422 | Alta | PASSED |
| TC-P10 | Campo precio ausente → HTTP 422 | Alta | PASSED |
| TC-P11 | Campo stock ausente → HTTP 422 | Alta | PASSED |
| TC-P12 | Nombre duplicado → HTTP 200 (sin restricción de unicidad) | Media | PASSED |
| TC-P13 | Producto aparece en GET /api/productos/ tras creación | Alta | PASSED |
| TC-P14 | Precio = 99999999.99 → HTTP 200, precio correcto | Baja | PASSED |

---

## 4. Defectos Encontrados

### DEF-003 — Nombre de usuario vacío aceptado
- **Test:** TC-U03  
- **Severidad:** Media  
- **Endpoint:** POST /api/usuarios/  
- **Descripción:** El sistema acepta crear un usuario con `nombre: ""`. No existe validación `min_length=1` en el schema `UsuarioCreate`.  
- **Comportamiento actual:** HTTP 200, usuario creado con nombre en blanco.  
- **Comportamiento esperado:** HTTP 422, error de validación indicando que el nombre no puede estar vacío.  
- **Causa probable:** Campo `nombre: str` en Pydantic sin restricción de longitud mínima.  
- **Corrección sugerida:** Cambiar a `nombre: str = Field(..., min_length=1, max_length=100)` en el schema.

---

### DEF-004 — Roles arbitrarios aceptados sin validación
- **Test:** TC-U05  
- **Severidad:** Alta  
- **Endpoint:** POST /api/usuarios/  
- **Descripción:** El sistema acepta cualquier string como valor del campo `rol`. Se creó un usuario con `rol: "supervisor"` sin ningún error.  
- **Comportamiento actual:** HTTP 200, usuario creado con rol personalizado.  
- **Comportamiento esperado:** HTTP 422, error indicando que el rol debe ser `"admin"` o `"vendedor"`.  
- **Causa probable:** Campo `rol: str` sin enum ni literal type en el schema.  
- **Corrección sugerida:** Usar `rol: Literal["admin", "vendedor"]` o un `Enum` en el schema `UsuarioCreate`.  
- **Impacto de seguridad:** Un atacante podría crear usuarios con roles inventados que pasen verificaciones de autorización mal implementadas.

---

### DEF-005 — Venta con cantidad = 0 aceptada
- **Test:** TC-V05  
- **Severidad:** Alta  
- **Endpoint:** POST /api/ventas/  
- **Descripción:** El sistema acepta registrar una venta con `cantidad: 0`, creando un detalle de venta con `subtotal: 0.0` y sin descontar stock.  
- **Comportamiento actual:** HTTP 200, venta registrada con cantidad cero.  
- **Comportamiento esperado:** HTTP 422, error de validación por cantidad no positiva.  
- **Causa probable:** El schema `DetalleVentaItem` no tiene la restricción `gt=0` en el campo `cantidad`, o el router no está usando el schema con esa restricción.  
- **Corrección sugerida:** Agregar `cantidad: int = Field(..., gt=0)` en el schema `DetalleVentaItem`.

---

### DEF-006 — Venta con cantidad negativa aceptada (total negativo)
- **Test:** TC-V06  
- **Severidad:** Alta  
- **Endpoint:** POST /api/ventas/  
- **Descripción:** El sistema acepta `cantidad: -1`, generando una venta con `total: -10.0`. Esto corrompe los registros contables y puede usarse para manipular totales.  
- **Comportamiento actual:** HTTP 200, venta con total negativo registrada en la base de datos.  
- **Comportamiento esperado:** HTTP 422, rechazo por cantidad negativa.  
- **Causa probable:** Misma raíz que DEF-005, sin validación de campo `cantidad`.  
- **Corrección sugerida:** Misma que DEF-005. Al corregir DEF-005, DEF-006 queda corregido también.  
- **Impacto:** Registros contables con totales negativos, posible explotación para revertir artificialmente el total de ventas.

---

### DEF-007 — Nombre de producto vacío aceptado
- **Test:** TC-P03  
- **Severidad:** Media  
- **Endpoint:** POST /api/productos/  
- **Descripción:** El sistema permite crear productos con `nombre: ""`. Misma raíz que DEF-003.  
- **Comportamiento actual:** HTTP 200, producto creado con nombre en blanco.  
- **Comportamiento esperado:** HTTP 400/422, error de validación.  
- **Causa probable:** Campo `nombre: str` en `ProductoCreate` sin `min_length=1`.  
- **Corrección sugerida:** `nombre: str = Field(..., min_length=1, max_length=200)` en el schema.

---

## 5. Matriz de Cobertura por Prioridad

| Prioridad | Total | Pasados | Fallados | % Éxito |
|---|---|---|---|---|
| Alta | 28 | 25 | 3 | 89.3 % |
| Media | 15 | 14 | 1 | 93.3 % |
| Baja | 5 | 5 | 0 | 100 % |
| **Total** | **48** | **43** | **5** | **89.6 %** |

---

## 6. Conclusiones

1. **El módulo de Login (F1) no presenta defectos.** Todas las validaciones de formato, autenticación y seguridad funcionan correctamente.

2. **El módulo de Ventas (F3) tiene la mayor criticidad:** Los defectos DEF-005 y DEF-006 permiten registrar ventas con cantidades cero o negativas, lo que genera registros contables inválidos. Deben corregirse con prioridad alta antes de producción.

3. **El módulo de Usuarios (F2) tiene una brecha de seguridad (DEF-004):** La ausencia de validación del campo `rol` permite crear usuarios con roles arbitrarios. Esto debe corregirse con un `Literal` o `Enum` en Pydantic.

4. **Los cálculos matemáticos son correctos:** Totales de ventas, subtotales, descuento de stock y manejo de precios decimales funcionan bien en todos los casos probados.

5. **Los defectos DEF-003 y DEF-007 comparten la misma causa raíz** (ausencia de `min_length` en strings obligatorios). Una corrección en la política de schemas de Pydantic resuelve ambos a la vez.

---

## 7. Correcciones Sugeridas (app/schemas.py)

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional

class UsuarioCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)   # DEF-003
    email: EmailStr
    password: str
    rol: Literal["admin", "vendedor"]                         # DEF-004

class ProductoCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200)   # DEF-007
    descripcion: Optional[str] = None
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)

class DetalleVentaItem(BaseModel):
    producto_id: int
    cantidad: int = Field(..., gt=0)                          # DEF-005 / DEF-006
    precio_unitario: float
```
