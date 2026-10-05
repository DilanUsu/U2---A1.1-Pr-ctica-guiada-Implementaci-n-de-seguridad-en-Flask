import os
import sys

from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from forms import RegistrationForm, LoginForm
from models import get_user_by_id, get_user_by_username, create_user

# Carga las variables del archivo .env (que NO se sube a Git)
load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SESSION_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_HTTPONLY'] = True

csrf = CSRFProtect(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        create_user(form.username.data, form.email.data, form.password.data)
        flash('Registro exitoso')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_username(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Inicio de sesión exitoso')
            return redirect(url_for('profile'))
        flash('Credenciales inválidas')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('Sesión cerrada')
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/secreto')
def secreto():
    if not current_user.is_authenticated:
        abort(401)
    return 'Contenido privado'


@app.route('/admin')
@login_required
def admin():
    if current_user.username != 'admin':
        abort(403)
    return 'Panel de administración'


@app.errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


if __name__ == '__main__':
    if '--http' in sys.argv:
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        app.run(ssl_context='adhoc', debug=True)
