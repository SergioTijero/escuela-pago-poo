# create_admin.py
from app import app, db
from models import Usuario
from werkzeug.security import generate_password_hash

def crear_admin():
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
        admin = Usuario(nombre_usuario='admin', contraseña=generate_password_hash('adminpass', method='pbkdf2:sha256'))
        db.session.add(admin)
        db.session.commit()
        print("Usuario administrador creado con nombre de usuario 'admin' y contraseña 'adminpass'")

if __name__ == '__main__':
    crear_admin()
