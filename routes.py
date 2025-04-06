from flask import (
    Blueprint,
    render_template,
    redirect,
    flash,
    url_for,
    session,
    request,
    current_app as app,
)
from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError

from flask_bcrypt import check_password_hash
from flask_login import (
    login_user,
    current_user,
    logout_user,
    login_required,
)

from app import db, login_manager, bcrypt
from models import User, Reserva
from forms import LoginForm, RegisterForm, RequestResetForm, ResetPasswordForm
from utils import (
    enviar_email_recuperacion,
    verificar_token,
    enviar_email_confirmacion,
    verificar_token_confirmacion,
)

# 🔧 Define el blueprint
routes = Blueprint("routes", __name__)

# 📌 Cargar usuario para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 📌 Mantener la sesión activa por 1 minuto
@routes.before_app_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)

# 🏠 Página principal
@routes.route("/", methods=["GET", "POST"], strict_slashes=False)
def index():
    return render_template("index.html", title="Home")

# 🔐 Login
@routes.route("/login/", methods=["GET", "POST"], strict_slashes=False)
def login():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.pwd, form.pwd.data):
                if not user.confirmado:
                    flash("Debes activar tu cuenta desde el correo antes de iniciar sesión.", "warning")
                    return redirect(url_for("routes.login"))
                login_user(user)
                return redirect(url_for("routes.index"))
            else:
                flash("Correo o contraseña inválidos.", "danger")
        except Exception as e:
            flash(str(e), "danger")

    return render_template(
        "auth.html",
        form=form,
        text="Login",
        title="Login",
        btn_action="Login"
    )

# 📝 Registro
@routes.route("/register/", methods=["GET", "POST"], strict_slashes=False)
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            email = form.email.data
            pwd = form.pwd.data
            username = form.username.data

            newuser = User(
                username=username,
                email=email,
                pwd=bcrypt.generate_password_hash(pwd).decode('utf-8'),
            )

            db.session.add(newuser)
            db.session.commit()

            enviar_email_confirmacion(newuser)

            flash("Cuenta creada correctamente. Revisa tu correo para activarla.", "info")
            return redirect(url_for("routes.login"))

        except InvalidRequestError:
            db.session.rollback()
            flash("¡Algo salió mal!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash("¡El usuario ya existe!", "warning")
        except DataError:
            db.session.rollback()
            flash("Entrada inválida.", "warning")
        except InterfaceError:
            db.session.rollback()
            flash("Error de conexión con la base de datos.", "danger")
        except DatabaseError:
            db.session.rollback()
            flash("Error de base de datos.", "danger")
        except BuildError as e:
            db.session.rollback()
            flash(f"Error de redireccionamiento: {str(e)}", "danger")
        except Exception as e:
            db.session.rollback()
            flash(f"Error inesperado: {str(e)}", "danger")

    return render_template(
        "auth.html",
        form=form,
        text="Crear cuenta",
        title="Registro",
        btn_action="Crear cuenta"
    )

# 🚪 Cerrar sesión
@routes.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("routes.login"))

# 🔁 Solicitud para restablecer contraseña
@routes.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("routes.index"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            enviar_email_recuperacion(user)
        flash("Se ha enviado un correo con instrucciones para restablecer tu contraseña.", "info")
        return redirect(url_for("routes.login"))
    return render_template("reset_request.html", form=form)

# 🔁 Restablecer contraseña con token
@routes.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("routes.index"))

    email = verificar_token(token)
    if email is None:
        flash("El enlace es inválido o ha expirado.", "warning")
        return redirect(url_for("routes.reset_request"))

    user = User.query.filter_by(email=email).first()
    if user is None:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for("routes.reset_request"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.pwd = hashed_password
        db.session.commit()
        flash("¡Tu contraseña ha sido actualizada! Ya puedes iniciar sesión", "success")
        return redirect(url_for("routes.login"))

    return render_template("reset_token.html", form=form)

# ✅ Confirmar cuenta desde correo
@routes.route("/confirmar_cuenta/<token>")
def confirmar_cuenta(token):
    user = verificar_token_confirmacion(token)
    if user is None:
        flash("El enlace de activación no es válido o ha expirado.", "danger")
        return redirect(url_for("routes.login"))

    if user.confirmado:
        flash("Tu cuenta ya está activada. Puedes iniciar sesión.", "info")
        return redirect(url_for("routes.login"))

    user.confirmado = True
    db.session.commit()
    flash("¡Cuenta activada exitosamente! Ya puedes iniciar sesión.", "success")
    return redirect(url_for("routes.login"))

@routes.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        current_user.pwd = hashed_password
        db.session.commit()
        flash("¡Tu contraseña ha sido actualizada exitosamente!", "success")
        return redirect(url_for("routes.index"))
    return render_template("reset_token.html", form=form, title="Change Password")


@routes.route("/buscar_vuelos", methods=["GET", "POST"])
@login_required
def buscar_vuelos():
    if request.method == "POST":
        origen = request.form.get("origen")
        destino = request.form.get("destino")
        fecha_salida = request.form.get("fecha_salida")
        num_pasajeros = request.form.get("num_pasajeros")

        # Aquí puedes implementar la lógica para buscar vuelos disponibles
        flash(f"Vuelos encontrados de {origen} a {destino} para {fecha_salida}.", "info")
        return redirect(url_for("routes.buscar_vuelos"))

    return render_template("buscar_vuelos.html", title="Buscar vuelos")

@routes.route("/reservar_vuelo", methods=["GET", "POST"])
@login_required
def reservar_vuelo():
    if request.method == "POST":
        origen = request.form.get("origen")
        destino = request.form.get("destino")
        fecha_salida = request.form.get("fecha_salida")
        num_pasajeros = request.form.get("num_pasajeros")

        nueva_reserva = Reserva(
            user_id=current_user.id,
            origen=origen,
            destino=destino,
            fecha_salida=fecha_salida,
            num_pasajeros=num_pasajeros,
            estado="Confirmado"
        )
        db.session.add(nueva_reserva)
        db.session.commit()
        flash("Vuelo reservado exitosamente.", "success")
        return redirect(url_for("routes.index"))

    return render_template("reservar_vuelo.html", title="Reservar vuelo")

@routes.route("/cancelar_reserva/<int:reserva_id>", methods=["POST"])
@login_required
def cancelar_reserva(reserva_id):
    reserva = Reserva.query.get_or_404(reserva_id)
    if reserva.user_id != current_user.id:
        flash("No tienes permiso para cancelar esta reserva.", "danger")
        return redirect(url_for("routes.index"))
    db.session.delete(reserva)
    db.session.commit()
    flash("Reserva cancelada exitosamente.", "success")
    return redirect(url_for("routes.index"))