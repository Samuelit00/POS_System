from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from .database import engine, Base, get_db
from .routers import users, products, sales
from . import models, schemas, crud

"""
Inicializa FASTAPI y permite definir las diferentes rutas
para direccionar las peticiones HTTP con la base de datos"""

app = FastAPI(title="POS System",
    description="API para gestionar ventas, usuarios, productos e inventario.",
    version="1.0.0")

# Create tables in development automatically
Base.metadata.create_all(bind=engine)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include API routers with /api prefix
app.include_router(users.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(sales.router, prefix="/api")

# Template Routes
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/productos", response_class=HTMLResponse)
async def productos_page(request: Request):
    return templates.TemplateResponse("productos.html", {"request": request})

@app.get("/pos", response_class=HTMLResponse)
async def pos_page(request: Request):
    return templates.TemplateResponse("pos.html", {"request": request})

@app.get("/inventario", response_class=HTMLResponse)
async def inventario_page(request: Request):
    return templates.TemplateResponse("inventario.html", {"request": request})

@app.get("/ventas", response_class=HTMLResponse)
async def ventas_page(request: Request):
    return templates.TemplateResponse("ventas.html", {"request": request})

@app.get("/usuarios", response_class=HTMLResponse)
async def usuarios_page(request: Request):
    return templates.TemplateResponse("usuarios.html", {"request": request})

@app.get("/reportes", response_class=HTMLResponse)
async def reportes_page(request: Request):
    return templates.TemplateResponse("reportes.html", {"request": request})

# Additional API endpoints for frontend
@app.get('/api/dashboard/metrics', response_model=schemas.DashboardMetrics)
def get_dashboard_metrics(db: Session = Depends(get_db)):
    today = datetime.now().date()
    
    # Ventas de hoy
    ventas_hoy = db.query(models.Venta).filter(
        models.Venta.fecha_creacion >= today,
        models.Venta.fecha_creacion < today + timedelta(days=1)
    ).all()
    
    total_ventas_hoy = sum(float(venta.total) for venta in ventas_hoy)
    ventas_count_hoy = len(ventas_hoy)
    
    # Productos con stock bajo (< 10)
    productos_bajo_stock = db.query(models.Producto).filter(models.Producto.stock < 10).count()
    
    # Usuarios activos
    usuarios_activos = db.query(models.Usuario).count()
    
    # Top productos vendidos (últimos 30 días)
    thirty_days_ago = today - timedelta(days=30)
    productos_top = db.query(
        models.Producto.nombre,
        func.sum(models.DetalleVenta.cantidad).label('cantidad'),
        func.sum(models.DetalleVenta.subtotal).label('total')
    ).join(
        models.DetalleVenta
    ).join(
        models.Venta
    ).filter(
        models.Venta.fecha_creacion >= thirty_days_ago
    ).group_by(
        models.Producto.id, models.Producto.nombre
    ).order_by(
        func.sum(models.DetalleVenta.cantidad).desc()
    ).limit(10).all()
    
    productos_top_list = [
        schemas.ProductoTop(
            nombre=item.nombre,
            cantidad=int(item.cantidad),
            total=float(item.total)
        ) for item in productos_top
    ]
    
    return schemas.DashboardMetrics(
        total_ventas_hoy=total_ventas_hoy,
        ventas_count_hoy=ventas_count_hoy,
        productos_bajo_stock=productos_bajo_stock,
        usuarios_activos=usuarios_activos,
        productos_top=productos_top_list
    )

@app.get('/health')
def health():
    return {'status': 'ok'}
