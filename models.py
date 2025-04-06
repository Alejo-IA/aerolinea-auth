from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer  # ✅ Actualizado
from flask import current_app
from app import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    confirmado = db.Column(db.Boolean, default=True)  # ✅ esta línea

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    origen = db.Column(db.String(100), nullable=False)
    destino = db.Column(db.String(100), nullable=False)
    fecha_salida = db.Column(db.Date, nullable=False)
    num_pasajeros = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(20), default="Pendiente")

    user = db.relationship('User', backref='reservas')


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=1800)['user_id']
        except Exception:
            return None
        return User.query.get(user_id)

    def get_confirm_token(self, expires_sec=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'confirm': self.id})

    @staticmethod
    def verify_confirm_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=3600)['confirm']
        except Exception:
            return None
        return User.query.get(user_id)
