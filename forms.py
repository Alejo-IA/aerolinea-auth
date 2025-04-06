from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import (
    InputRequired,
    Length,
    EqualTo,
    Email,
    Regexp,
    Optional,
    ValidationError,
)
from models import User


# -----------------------------
# Formulario de Login
# -----------------------------
class LoginForm(FlaskForm):
    email = StringField(
        "Correo electrónico",
        validators=[InputRequired(message="Requerido"), Email(), Length(1, 64)],
    )
    pwd = PasswordField(
        "Contraseña",
        validators=[InputRequired(), Length(min=8, max=72)],
    )


# -----------------------------
# Formulario de Registro
# -----------------------------
class RegisterForm(FlaskForm):
    username = StringField(
        "Nombre de usuario",
        validators=[
            InputRequired(),
            Length(3, 20, message="Debe tener entre 3 y 20 caracteres"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Solo se permiten letras, números, puntos o guiones bajos",
            ),
        ],
    )
    email = StringField(
        "Correo electrónico",
        validators=[InputRequired(), Email(), Length(1, 64)],
    )
    pwd = PasswordField(
        "Contraseña",
        validators=[InputRequired(), Length(8, 72)],
    )
    cpwd = PasswordField(
        "Confirmar contraseña",
        validators=[
            InputRequired(),
            EqualTo("pwd", message="¡Las contraseñas deben coincidir!"),
        ],
    )

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("¡Este correo ya está registrado!")

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("¡El nombre de usuario ya está en uso!")


# -----------------------------
# Paso 1: Solicitud de recuperación
# -----------------------------
class RequestResetForm(FlaskForm):
    email = StringField(
        "Correo electrónico",
        validators=[InputRequired(), Email(), Length(1, 64)],
    )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("No existe una cuenta con ese correo electrónico.")


# -----------------------------
# Paso 2: Nueva contraseña
# -----------------------------
class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "Nueva contraseña",
        validators=[
            InputRequired(),
            Length(min=8, max=72, message="Debe tener mínimo 8 caracteres"),
        ],
    )
    confirm_password = PasswordField(
        "Confirmar nueva contraseña",
        validators=[
            InputRequired(),
            EqualTo("password", message="¡Las contraseñas deben coincidir!"),
        ],
    )
