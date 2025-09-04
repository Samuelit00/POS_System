from fastapi import FastAPI
from .database import engine, Base
from .routers import users, products, sales


"""
Inicializa FASTAPI y permite definir las diferentes rutas
para direccionar las peticiones HTTP con la base de datos"""

app = FastAPI(title="POS System",
    description="API para gestionar ventas, usuarios, productos e inventario.",
    version="1.0.0")

# Create tables in development automatically



Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(products.router)
app.include_router(sales.router)

@app.get('/health')
def health():
    return {'status': 'ok'}
