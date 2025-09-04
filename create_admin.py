
# Script útil para crear un admin inicial localmente.
from app.database import SessionLocal
from app import models
from app.utils.security import hash_password

def create_admin():
    db = SessionLocal()
    try:
        email = 'admin@pos.local'
        existing = db.query(models.Usuario).filter(models.Usuario.email == email).first()
        if existing:
            print('Admin ya existe:', email)
            return
        admin = models.Usuario(nombre='Admin', email=email, password_hash=hash_password('admin123'), rol='admin')
        db.add(admin)
        db.commit()
        print('Admin creado:', email, 'contraseña: admin123')
    finally:
        db.close()

if __name__ == '__main__':
    create_admin()
