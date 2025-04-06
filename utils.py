from itsdangerous import URLSafeTimedSerializer
from flask import current_app, url_for
from flask_mail import Message
from app import mail
from models import User

# ---------------------- 🔐 UTILIDADES GENERALES DE TOKENS ----------------------

def _generar_serializer():
    """Crea y devuelve una instancia del serializador con la clave secreta."""
    return URLSafeTimedSerializer(current_app.secret_key)

# ---------------------- 🔁 RECUPERACIÓN DE CONTRASEÑA ----------------------

def generar_token(email):
    """Genera un token firmado con vencimiento (para recuperación de contraseña)."""
    serializer = _generar_serializer()
    return serializer.dumps(email, salt='recuperar-password')

def verificar_token(token, expiracion=3600):
    """Verifica el token de recuperación y devuelve el email si es válido."""
    serializer = _generar_serializer()
    try:
        return serializer.loads(token, salt='recuperar-password', max_age=expiracion)
    except Exception as e:
        print("❌ Token inválido o expirado:", str(e))
        return None

def enviar_email_recuperacion(usuario):
    """Envía un correo con el enlace para restablecer la contraseña."""
    token = generar_token(usuario.email)
    link = url_for('routes.reset_token', token=token, _external=True)

    mensaje = Message("🔑 Recupera tu contraseña",
                      recipients=[usuario.email])
    mensaje.body = f"""Hola {usuario.username},

Has solicitado restablecer tu contraseña. Para continuar, haz clic en el siguiente enlace:

{link}

Si no solicitaste este cambio, puedes ignorar este mensaje.

— Tu App
"""
    try:
        mail.send(mensaje)
        print(f"✅ Correo de recuperación enviado a {usuario.email}")
    except Exception as e:
        print(f"❌ Error al enviar correo de recuperación a {usuario.email}: {e}")

# ---------------------- ✅ ACTIVACIÓN DE CUENTA ----------------------

def generar_token_confirmacion(email):
    """Genera un token firmado con vencimiento (para activar cuenta)."""
    serializer = _generar_serializer()
    return serializer.dumps(email, salt='activar-cuenta')

def verificar_token_confirmacion(token, expiracion=3600):
    """Verifica el token de activación y devuelve el usuario si es válido."""
    serializer = _generar_serializer()
    try:
        email = serializer.loads(token, salt='activar-cuenta', max_age=expiracion)
        return User.query.filter_by(email=email).first()
    except Exception as e:
        print("❌ Token de activación inválido o expirado:", str(e))
        return None

def enviar_email_confirmacion(usuario):
    token = generar_token_confirmacion(usuario.email)
    link = url_for('routes.confirmar_cuenta', token=token, _external=True)

    print(f"🔗 Token generado: {token}")
    print(f"🔗 Enlace de activación: {link}")

    mensaje = Message('Activa tu cuenta', recipients=[usuario.email])
    mensaje.body = f'''Hola {usuario.username},

Gracias por registrarte. Para activar tu cuenta, haz clic en el siguiente enlace:

{link}

Si no te registraste en nuestra aplicación, puedes ignorar este mensaje.

– Tu App
'''

    try:
        print(f"📧 Enviando correo a: {usuario.email}")
        mail.send(mensaje)
        print("✅ Correo de activación enviado correctamente")
    except Exception as e:
        print("❌ Error al enviar correo de activación:", str(e))
        raise e
    
