from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Config
from forms import FormularioPago, FormularioBusqueda, FormularioLogin, FormularioEditarAlumno, FormularioEditarPago
from models import db, Usuario, Alumno, Pago
import sqlalchemy.exc

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = FormularioLogin()
    if form.validate_on_submit():
        try:
            user = Usuario.query.filter_by(nombre_usuario=form.nombre_usuario.data).first()
            if user and check_password_hash(user.contraseña, form.contraseña.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Inicio de sesión no exitoso. Por favor, verifique su nombre de usuario y contraseña.', 'danger')
        except sqlalchemy.exc.OperationalError:
            flash('Error de conexión a la base de datos. Por favor, intente nuevamente más tarde.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    pago_form = FormularioPago()
    busqueda_form = FormularioBusqueda()
    if pago_form.validate_on_submit():
        alumno = Alumno.query.filter_by(nombre=pago_form.nombre_alumno.data, nombre_apoderado=pago_form.nombre_apoderado.data).first()
        if not alumno:
            alumno = Alumno(nombre=pago_form.nombre_alumno.data, nombre_apoderado=pago_form.nombre_apoderado.data)
            db.session.add(alumno)
            db.session.commit()
        pago = Pago(alumno_id=alumno.id, monto=pago_form.monto.data, concepto=pago_form.concepto.data, fecha_hora=datetime.now())
        db.session.add(pago)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', pago_form=pago_form, busqueda_form=busqueda_form)

@app.route('/buscar', methods=['GET', 'POST'])
@login_required
def buscar():
    form = FormularioBusqueda()
    alumnos = []
    if form.validate_on_submit():
        termino_busqueda = form.busqueda.data
        alumnos = Alumno.query.filter(
            db.or_(Alumno.nombre.ilike(f'%{termino_busqueda}%'), Alumno.nombre_apoderado.ilike(f'%{termino_busqueda}%'))
        ).all()
    return render_template('buscar.html', form=form, alumnos=alumnos)

@app.route('/alumno/<uuid:alumno_id>')
@login_required
def detalle_alumno(alumno_id):
    alumno = Alumno.query.get_or_404(alumno_id)
    pagos = Pago.query.filter_by(alumno_id=alumno.id).all()
    form = FormularioPago()
    return render_template('detalle_alumno.html', alumno=alumno, pagos=pagos, form=form)

@app.route('/alumno/editar/<uuid:alumno_id>', methods=['GET', 'POST'])
@login_required
def editar_alumno(alumno_id):
    alumno = Alumno.query.get_or_404(alumno_id)
    form = FormularioEditarAlumno(obj=alumno)
    if form.validate_on_submit():
        alumno.nombre = form.nombre.data
        alumno.nombre_apoderado = form.nombre_apoderado.data
        db.session.commit()
        flash('Alumno actualizado exitosamente', 'success')
        return redirect(url_for('detalle_alumno', alumno_id=alumno.id))
    return render_template('editar_alumno.html', form=form, alumno=alumno)

@app.route('/pago/editar/<int:pago_id>', methods=['GET', 'POST'])
@login_required
def editar_pago(pago_id):
    pago = Pago.query.get_or_404(pago_id)
    form = FormularioEditarPago(obj=pago)
    if form.validate_on_submit():
        pago.monto = form.monto.data
        pago.concepto = form.concepto.data
        db.session.commit()
        flash('Pago actualizado exitosamente', 'success')
        return redirect(url_for('detalle_alumno', alumno_id=pago.alumno_id))
    return render_template('editar_pago.html', form=form, pago=pago)

@app.route('/alumno/<uuid:alumno_id>/añadir_pago', methods=['POST'])
@login_required
def añadir_pago(alumno_id):
    form = FormularioPago()
    alumno = Alumno.query.get_or_404(alumno_id)
    if form.validate_on_submit():
        pago = Pago(alumno_id=alumno.id, monto=form.monto.data, concepto=form.concepto.data, fecha_hora=datetime.now())
        db.session.add(pago)
        db.session.commit()
        flash('Pago añadido exitosamente', 'success')
    return redirect(url_for('detalle_alumno', alumno_id=alumno.id))

if __name__ == '__main__':
    app.run(debug=True)
