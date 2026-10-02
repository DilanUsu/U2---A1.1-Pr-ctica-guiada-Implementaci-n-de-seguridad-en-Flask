from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError

from models import get_user_by_username


class RegistrationForm(FlaskForm):
    username = StringField(
        "Usuario",
        validators=[DataRequired(message="Escribe un nombre de usuario."),
                    Length(min=3, max=20, message="Debe tener entre 3 y 20 caracteres.")])
    email = EmailField(
        "Correo",
        validators=[DataRequired(message="Escribe tu correo.")])
    password = PasswordField(
        "Contraseña",
        validators=[DataRequired(message="Escribe una contraseña."),
                    Length(min=6, message="Debe tener al menos 6 caracteres.")])
    confirm_password = PasswordField(
        "Confirmar contraseña",
        validators=[DataRequired(message="Confirma la contraseña."),
                    EqualTo("password", message="Las contraseñas no coinciden.")])
    submit = SubmitField("Crear cuenta")

    def validate_username(self, field):
        if get_user_by_username(field.data):
            raise ValidationError("Ese usuario ya existe.")


class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(message="Escribe tu usuario.")])
    password = PasswordField("Contraseña", validators=[DataRequired(message="Escribe tu contraseña.")])
    submit = SubmitField("Iniciar sesión")
