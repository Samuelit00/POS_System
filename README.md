
# POS XYZ - FastAPI minimal scaffold

Proyecto base minimal para un POS con FastAPI + PostgreSQL (esqueleto para desarrollo local).

Contenido:

- app/: código fuente (models, routers, crud, utils)
- schema.sql: script SQL opcional para crear tablas manualmente
- create_admin.py: script para crear un admin inicial localmente
- .env.example: variables de entorno (no subir .env con credenciales reales a GitHub)
- requirements.txt: dependencias


Instrucciones rápidas (local):
1. Crear virtualenv e instalar dependencias:
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt

2. Configurar DB en .env (usa .env.example como plantilla)
3. Crear la base y usuario en PostgreSQL (si no lo hiciste):
   psql -U postgres
   CREATE DATABASE pos_db;
   CREATE USER pos_user WITH PASSWORD 'pos_password';
   GRANT ALL PRIVILEGES ON DATABASE pos_db TO pos_user;
   \q

4. Ejecutar la app:
   uvicorn app.main:app --reload

5. Abrir Swagger UI en http://127.0.0.1:8000/docs

Nota: este scaffold usa SQLAlchemy y Base.metadata.create_all() para crear tablas en desarrollo.
Para producción usa Alembic para migraciones.
