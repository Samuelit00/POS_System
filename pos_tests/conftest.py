import uuid
import pytest
import requests

BASE_URL = "http://localhost:8000"

ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin123"

VENDEDOR_EMAIL_BASE = "vendedor_test"
VENDEDOR_PASSWORD = "vendedor123"


def email_unico(prefijo: str = "test") -> str:
    """Genera un email único con UUID para evitar conflictos entre ejecuciones."""
    return f"{prefijo}_{uuid.uuid4().hex[:8]}@test.com"


def _login(email: str, password: str) -> dict:
    r = requests.post(f"{BASE_URL}/api/usuarios/login", json={"email": email, "password": password})
    assert r.status_code == 200, f"Login falló para {email}: {r.status_code} {r.text}"
    return r.json()


def _auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# admin_existente — garantiza que el admin existe y devuelve su token
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def admin_existente():
    """Verifica que el admin por defecto existe (creado por create_admin.py)."""
    data = _login(ADMIN_EMAIL, ADMIN_PASSWORD)
    return {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD,
        "token": data["access_token"],
    }


# ---------------------------------------------------------------------------
# vendedor_existente — crea (o reutiliza) un vendedor de prueba
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def vendedor_existente(admin_existente):
    """Crea un usuario vendedor de prueba; devuelve sus datos y token."""
    email = email_unico("vendedor_sess")
    payload = {
        "nombre": "Vendedor Test",
        "email": email,
        "password": VENDEDOR_PASSWORD,
        "rol": "vendedor",
    }
    r = requests.post(f"{BASE_URL}/api/usuarios/", json=payload)
    assert r.status_code == 200, f"No se pudo crear vendedor: {r.status_code} {r.text}"
    user = r.json()
    token_data = _login(email, VENDEDOR_PASSWORD)
    return {
        "id": user["id"],
        "email": email,
        "password": VENDEDOR_PASSWORD,
        "token": token_data["access_token"],
    }


# ---------------------------------------------------------------------------
# producto_con_stock — crea un producto con stock=50, precio=1000
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def producto_con_stock(admin_existente):
    """Crea un producto con stock=50 y precio=1000 para tests de ventas."""
    payload = {
        "nombre": f"Prod Stock {uuid.uuid4().hex[:6]}",
        "descripcion": "Producto de prueba con stock",
        "precio": 1000.0,
        "stock": 50,
    }
    r = requests.post(f"{BASE_URL}/api/productos/", json=payload)
    assert r.status_code == 200, f"No se pudo crear producto con stock: {r.status_code} {r.text}"
    return r.json()


# ---------------------------------------------------------------------------
# producto_precio_decimal — crea producto con precio=99.99
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def producto_precio_decimal(admin_existente):
    """Crea un producto con precio=99.99 para tests de decimales."""
    payload = {
        "nombre": f"Prod Decimal {uuid.uuid4().hex[:6]}",
        "descripcion": "Producto con precio decimal",
        "precio": 99.99,
        "stock": 20,
    }
    r = requests.post(f"{BASE_URL}/api/productos/", json=payload)
    assert r.status_code == 200, f"No se pudo crear producto decimal: {r.status_code} {r.text}"
    return r.json()


# ---------------------------------------------------------------------------
# usuario_id_valido — devuelve el ID del admin (siempre existe)
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def usuario_id_valido(admin_existente):
    """Obtiene el ID del admin como usuario siempre existente."""
    r = requests.get(f"{BASE_URL}/api/usuarios/")
    assert r.status_code == 200, f"No se pudo listar usuarios: {r.status_code} {r.text}"
    usuarios = r.json()
    admin = next((u for u in usuarios if u["email"] == ADMIN_EMAIL), None)
    assert admin is not None, "No se encontró el admin en la lista de usuarios"
    return admin["id"]
