from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import uuid
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(150), unique=True, nullable=False)
    contraseña = db.Column(db.String(150), nullable=False)

class Alumno(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = db.Column(db.String(100), nullable=False)
    nombre_apoderado = db.Column(db.String(100), nullable=False)
    pagos = db.relationship('Pago', backref='alumno', lazy=True)

class Pago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(UUID(as_uuid=True), db.ForeignKey('alumno.id'), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    concepto = db.Column(db.String(100), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False)
