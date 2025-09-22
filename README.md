# 🛍️ POS XYZ System - Sistema de Punto de Venta

# POS XYZ - FastAPI minimal scaffold

Un sistema completo de Punto de Venta desarrollado con **FastAPI** (backend) y **Bootstrap 5** (frontend) con autenticación JWT y base de datos PostgreSQL.

Proyecto base minimal para un POS con FastAPI + PostgreSQL (esqueleto para desarrollo local).

## 📋 Características

Contenido:

### ✨ Funcionalidades Principales

- **🔐 Autenticación y Autorización**: Login seguro con JWT y roles (Admin/Vendedor)- app/: código fuente (models, routers, crud, utils)

- **🛒 Punto de Venta (POS)**: Interfaz intuitiva para procesar ventas- schema.sql: script SQL opcional para crear tablas manualmente

- **📦 Gestión de Productos**: CRUD completo de productos con control de stock- create_admin.py: script para crear un admin inicial localmente

- **📊 Inventario**: Seguimiento en tiempo real del stock con alertas- .env.example: variables de entorno (no subir .env con credenciales reales a GitHub)

- **💳 Historial de Ventas**: Registro completo con filtros y detalles- requirements.txt: dependencias

- **👥 Gestión de Usuarios**: Administración de usuarios y roles

- **📈 Dashboard**: Métricas y gráficos en tiempo real

- **📋 Reportes**: Análisis de ventas y estadísticas avanzadasInstrucciones rápidas (local):

1. Crear virtualenv e instalar dependencias:

### 🎯 Características Técnicas   python -m venv venv

- **Backend**: FastAPI con SQLAlchemy ORM   source venv/bin/activate   # Windows: venv\Scripts\activate

- **Frontend**: HTML5, Bootstrap 5, JavaScript ES6+   pip install -r requirements.txt

- **Base de Datos**: PostgreSQL

- **Autenticación**: JWT (JSON Web Tokens)2. Configurar DB en .env (usa .env.example como plantilla)

- **Gráficos**: Chart.js para visualizaciones3. Crear la base y usuario en PostgreSQL (si no lo hiciste):

- **Responsive**: Compatible con dispositivos móviles   psql -U postgres

   CREATE DATABASE pos_db;

## 🚀 Instalación y Configuración   CREATE USER pos_user WITH PASSWORD 'pos_password';

   GRANT ALL PRIVILEGES ON DATABASE pos_db TO pos_user;

### 📋 Prerrequisitos   \q



Asegúrate de tener instalado:4. Ejecutar la app:

- **Python 3.8+** ([Descargar Python](https://python.org))   uvicorn app.main:app --reload

- **PostgreSQL 12+** ([Descargar PostgreSQL](https://postgresql.org))

- **Git** ([Descargar Git](https://git-scm.com))5. Abrir Swagger UI en http://127.0.0.1:8000/docs



### 1️⃣ Clonar el RepositorioNota: este scaffold usa SQLAlchemy y Base.metadata.create_all() para crear tablas en desarrollo.

Para producción usa Alembic para migraciones.

```bash
git clone https://github.com/tuusuario/POS_System.git
cd POS_System
```

### 2️⃣ Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3️⃣ Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar Base de Datos

#### Crear Base de Datos en PostgreSQL:
```sql
-- Conectarse a PostgreSQL como superusuario
CREATE DATABASE pos_db;
CREATE USER pos_user WITH PASSWORD 'pos_password';
GRANT ALL PRIVILEGES ON DATABASE pos_db TO pos_user;
```

#### Ejecutar Script de Schema:
```bash
# Conectarse a PostgreSQL y ejecutar:
psql -U pos_user -d pos_db -f schema.sql
```

### 5️⃣ Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env
```

Editar el archivo `.env` con tus configuraciones:
```bash
DATABASE_URL=postgresql://pos_user:pos_password@localhost:5432/pos_db
SECRET_KEY=tu-clave-secreta-muy-larga-y-segura-aqui-cambiarla
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 6️⃣ Crear Usuario Administrador

```bash
python create_admin.py
```

Ingresa los datos solicitados:
- **Nombre**: Tu nombre completo
- **Email**: tu@email.com
- **Contraseña**: Una contraseña segura

### 7️⃣ Iniciar el Servidor

```bash
# Modo desarrollo
uvicorn app.main:app --reload

# Modo producción
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 8️⃣ Acceder al Sistema

Abre tu navegador en: **http://localhost:8000**

**Credenciales de prueba:**
- **Email**: El email que configuraste en el paso 6
- **Contraseña**: La contraseña que configuraste en el paso 6

## 📁 Estructura del Proyecto

```
POS_System/
├── app/                          # Aplicación principal
│   ├── __init__.py
│   ├── main.py                   # Punto de entrada FastAPI
│   ├── database.py               # Configuración de base de datos
│   ├── models.py                 # Modelos SQLAlchemy
│   ├── schemas.py                # Esquemas Pydantic
│   ├── crud/                     # Operaciones CRUD
│   │   ├── products.py
│   │   ├── sales.py
│   │   ├── users.py
│   │   └── seed.py
│   ├── routers/                  # Endpoints API
│   │   ├── products.py
│   │   ├── sales.py
│   │   └── users.py
│   ├── utils/                    # Utilidades
│   │   ├── jwt.py                # Manejo JWT
│   │   └── security.py          # Seguridad
│   ├── static/                   # Archivos estáticos
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/                # Plantillas HTML
│       ├── base.html
│       ├── dashboard.html
│       ├── pos.html
│       └── ...
├── tests/                        # Tests
├── venv/                         # Entorno virtual
├── .env.example                  # Variables de entorno ejemplo
├── requirements.txt              # Dependencias Python
├── schema.sql                    # Schema de base de datos
├── create_admin.py              # Script crear admin
└── README.md                     # Este archivo
```

## 🎮 Uso del Sistema

### 🔐 1. Autenticación
- Accede con las credenciales del administrador creado
- El sistema mantiene la sesión activa con JWT

### 🛒 2. Punto de Venta (POS)
1. Navega a **"Punto de Venta"**
2. Busca y selecciona productos
3. Ajusta cantidades en el carrito
4. Procesa la venta
5. Genera recibo automáticamente

### 📦 3. Gestión de Productos
1. Ve a **"Productos"**
2. **Crear**: Click "Nuevo Producto"
3. **Editar**: Click en el producto
4. **Eliminar**: Botón de eliminar (requiere confirmación)

### 👥 4. Gestión de Usuarios (Solo Admin)
1. Accede a **"Usuarios"**
2. Crea vendedores con email/contraseña
3. Administra roles y permisos

### 📊 5. Dashboard y Reportes
- **Dashboard**: Métricas en tiempo real
- **Reportes**: Análisis detallado de ventas
- **Inventario**: Control de stock y alertas

## 🛠️ API Endpoints

### 🔐 Autenticación
```
POST /auth/login          # Iniciar sesión
POST /auth/logout         # Cerrar sesión
```

### 👥 Usuarios
```
GET    /usuarios/         # Listar usuarios
POST   /usuarios/         # Crear usuario
DELETE /usuarios/{id}     # Eliminar usuario
```

### 📦 Productos
```
GET    /productos/        # Listar productos
POST   /productos/        # Crear producto
PUT    /productos/{id}    # Actualizar producto
DELETE /productos/{id}    # Eliminar producto
```

### 💳 Ventas
```
GET    /ventas/           # Listar ventas
POST   /ventas/           # Crear venta
GET    /ventas/{id}       # Obtener venta específica
```

### 📊 Dashboard
```
GET    /dashboard/metrics # Métricas del dashboard
```

## 🔧 Configuración Avanzada

### 🔒 Seguridad
- Cambia el `SECRET_KEY` en producción
- Usa HTTPS en producción
- Configura CORS según necesidades
- Actualiza contraseñas regularmente

### 🌐 Producción
Para despliegue en producción:
1. Configura un servidor web (Nginx)
2. Usa un servidor WSGI (Gunicorn)
3. Configura SSL/HTTPS
4. Usa una base de datos remota
5. Configura logs y monitoreo

## 🧪 Testing

```bash
# Ejecutar tests
python -m pytest tests/

# Con cobertura
python -m pytest --cov=app tests/
```

## 🤝 Contribución

1. Fork del proyecto
2. Crea una rama feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abrir Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👥 Autores

- **Tu Nombre** - *Desarrollo inicial* - [TuUsuario](https://github.com/tuusuario)

## 🙏 Agradecimientos

- FastAPI por el excelente framework
- Bootstrap por la UI responsiva
- Chart.js por las visualizaciones
- SQLAlchemy por el ORM robusto

## 📞 Soporte

Si tienes problemas o preguntas:
1. Revisa la [documentación](#-uso-del-sistema)
2. Busca en [Issues](https://github.com/tuusuario/POS_System/issues)
3. Crea un nuevo issue si es necesario

---
⭐ **¡Si te gusta este proyecto, dale una estrella!** ⭐