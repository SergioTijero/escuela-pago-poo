# create_admin.py

from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def create_admin():
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
        admin = User(username='admin', password=generate_password_hash('adminpass', method='sha256'))
        db.session.add(admin)
        db.session.commit()
        print("Admin user created with username 'admin' and password 'adminpass'")

if __name__ == '__main__':
    create_admin()
