# 🛍️ POS XYZ System - Sistema de Punto de Venta

Un sistema completo de Punto de Venta desarrollado con **FastAPI** (backend) y **Bootstrap 5** (frontend) con autenticación JWT y base de datos PostgreSQL.

Este proyecto base minimal para un POS funciona como esqueleto para desarrollo local, ideal para levantar de forma rápida un sistema de administración de ventas y caja.

## 📋 Características

### ✨ Funcionalidades Principales
- **🔐 Autenticación y Autorización**: Login seguro con JWT y roles (Admin/Vendedor).
- **🛒 Punto de Venta (POS)**: Interfaz intuitiva para procesar ventas ágilmente.
- **📦 Gestión de Productos**: CRUD completo de productos con control de stock.
- **📊 Inventario**: Seguimiento en tiempo real del stock con alertas.
- **💳 Historial de Ventas**: Registro completo con filtros y detalles.
- **👥 Gestión de Usuarios**: Administración de usuarios con distintos roles y permisos.
- **📈 Dashboard**: Métricas y gráficos de ventas en tiempo real.
- **📋 Reportes**: Análisis de ventas y estadísticas avanzadas.

### 🎯 Características Técnicas
- **Backend**: FastAPI con SQLAlchemy ORM.
- **Frontend**: HTML5, Bootstrap 5, JavaScript ES6+.
- **Base de Datos**: PostgreSQL 12+.
- **Autenticación**: JWT (JSON Web Tokens).
- **Gráficos**: Chart.js para visualizaciones en dashboards.
- **Responsive**: Interfaz totalmente adaptable y compatible con dispositivos móviles.


## 🚀 Guía de Instalación y Configuración Paso a Paso

Sigue estas instrucciones detalladas para inicializar el proyecto en un computador nuevo, configurando la base de datos y todas las variables de entorno necesarias.

### 📋 Prerrequisitos
Asegúrate de tener instalados los siguientes programas en tu computador:
- **Python 3.8+**: Asegúrate de marcar "Add Python to PATH" durante la instalación ([Descargar Python](https://python.org)).
- **PostgreSQL 12+**: Y la herramienta de línea de comandos `psql` ([Descargar PostgreSQL](https://postgresql.org)). En la mayoría de OS, `psql` ya viene con Postgres. En Windows puede que debas agregar la carpeta de `bin` de Postgres a las Variables de Entorno del sistema.
- **Git** ([Descargar Git](https://git-scm.com)).

---

### 1️⃣ Clonar el Repositorio
Abre tu terminal, PowerShell o Git Bash.
```bash
git clone https://github.com/tuusuario/POS_System.git
cd POS_System
```

### 2️⃣ Crear y Activar el Entorno Virtual
Se recomienda aislar las dependencias del proyecto creando un entorno virtual (`venv`).

```bash
# 1. Crear entorno virtual llamado "venv"
python -m venv venv

# 2. Activar entorno virtual
# En Windows (PowerShell/CMD):
venv\Scripts\activate
# En Linux/Mac (Bash):
source venv/bin/activate
```

### 3️⃣ Instalar Dependencias
Una vez activado el entorno (verás un `(venv)` al inicio de tu línea de comandos):
```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar la Base de Datos en PostgreSQL
Debemos crear una base de datos exclusiva para la aplicación y un usuario con permisos. 

Abre una **nueva pestaña** en tu terminal (para no cerrar el entorno de Python) y ejecuta `psql` con el usuario principal `postgres`:

```bash
# Conectarse a PostgreSQL como administrador. 
# Te pedirá la contraseña que configuraste al instalar PostgreSQL.
psql -U postgres
```

Dentro de la terminal/consola de `psql` (el prompt será algo como `postgres=#`), ejecuta uno por uno los siguientes comandos (no olvides el punto y coma final `;`):

```sql
-- 1. Crear la base de datos
CREATE DATABASE pos_db;

-- 2. Crear un usuario exclusivo y su contraseña
CREATE USER pos_user WITH PASSWORD 'pos_password';

-- 3. Dar privilegios del dueño al nuevo usuario
GRANT ALL PRIVILEGES ON DATABASE pos_db TO pos_user;

-- 4. Salir de psql
\q
```

**Nota sobre la estructura (Schema SQL):** 
El proyecto está configurado con `SQLAlchemy` para crear las tablas automáticamente si no existen (`Base.metadata.create_all`). No es necesario que corras el archivo `schema.sql` por defecto. Si en caso extremo necesitas crearlas a mano utilizando el script:
```bash
# (Opcional) Construir tablas de la BD manual
psql -U pos_user -d pos_db -f schema.sql
```

### 5️⃣ Configurar Variables de Entorno (.env)
El proyecto utiliza un archivo oculto `.env` para obtener contraseñas y configuraciones sensibles sin guardarlas publicamente.

```bash
# Copiar el archivo de plantilla a nuestro archivo definitivo real (.env)
# En bash/linux/mac/Git-Bash:
cp .env.example .env
# En PowerShell Windows:
Copy-Item .env.example .env
```

Abre el archivo `.env` recién creado en VS Code o tu editor favorito. Verifica que las credenciales coincidan con las que creaste en el paso 4.
```env
# Debe ser en este formato postgresql://usuario:contraseña@servidor:puerto/base_de_datos
DATABASE_URL=postgresql://pos_user:pos_password@localhost:5432/pos_db

# Crea una contraseña al azar muy segura y cámbiala aquí
SECRET_KEY=cambia-esto-por-un-texto-super-largo-al-azar
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 6️⃣ Crear el Primer Usuario Administrador
Antes de abrir el sistema en navegador, requieres un usuario inicial para ingresar al Punto de Venta. Utiliza el script que provee el proyecto:

```bash
python create_admin.py
```

Sigue las instrucciones en consola:
- **Nombre**: Ingresa tu nombre (Ej. Administrador Principal).
- **Email**: Ingresa un correo electrónico fácil de recordar (Ej. admin@pos.com).
- **Contraseña**: Escribe una contraseña segura (se guardará cifrada).

### 7️⃣ Iniciar el Servidor Principal FastAPI
Con tu entorno virtual aún activo, corre la aplicación con `uvicorn`:

```bash
# Modo desarrollo con recarga automática en caso de cambiar el código
uvicorn app.main:app --reload

# Si prefieres correrlo limpio (sin recarga al modificar arhivos)
# uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 8️⃣ Acceder al Sistema
1. Abre tu navegador favorito y dirígete a: **http://localhost:8000**
2. Inicia sesión con el correo electrónico (Email) y Contraseña que creaste en el paso anterior.
3. Puedes ver y probar la API directamente de forma visual ingresando en **http://localhost:8000/docs** (Swagger UI).

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