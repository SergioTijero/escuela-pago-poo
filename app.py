# app.py
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Config
from forms import PaymentForm, LoginForm
from models import db, User, Student, Payment
import sqlalchemy.exc

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        except sqlalchemy.exc.OperationalError:
            flash('Database connection failed. Please try again later.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = PaymentForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(name=form.student_name.data, guardian_name=form.guardian_name.data).first()
        if not student:
            student = Student(name=form.student_name.data, guardian_name=form.guardian_name.data)
            db.session.add(student)
            db.session.commit()
        payment = Payment(student_id=student.id, amount=form.amount.data, concept=form.concept.data, date_time=datetime.now())
        db.session.add(payment)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
