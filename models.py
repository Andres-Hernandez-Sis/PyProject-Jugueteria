import jwt
import datetime
from config import BaseConfig
from app import db, bcrypt

class User(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    telefono = db.Column(db.String(255), unique=True, nullable=False)
    permisos_admin = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    def __init__(self,id,nombre, email,telefono,permisos_admin, password) -> None:
        self.email = email
        self.password = bcrypt.generate_password_hash(password, BaseConfig.BCRYPT_LOG_ROUND).decode()
        self.registered_on = datetime.datetime.now()
        self.permisos_admin = permisos_admin

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=10),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(payload, BaseConfig.SECRET_KEY, algorithm="HS256")
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, BaseConfig.SECRET_KEY, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError as e:
            return "Token Expirado"
        except jwt.InvalidTokenError as e:
            return "Token No Valido"


class Proveedor(db.Model):
    __tablename__ = "proveedor"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), unique=True, nullable=False)
    telefono = db.Column(db.String(255), unique=True, nullable=False)
    marca = db.Column(db.String(255), unique=True, nullable=False)
    juguetes = db.relationship("Juguete", back_populates = "proveedor")


class Juguete(db.Model):
    __tablename__ = "juguete"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), unique=True, nullable=False)
    costo = db.Column(db.Integer, unique=True, nullable=False)
    cantidad = db.Column(db.Integer, unique=True, nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
    proveedor = db.relationship('Proveedor', back_populates = "juguetes")


class Juguete_Imagen(db.Model):
    __tablename__ = "juguete_imagen"
    id_imagen = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(128), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    renderate_date = db.Column(db.Text, nullable=False)
    juguete_id = db.Column(db.Integer, db.ForeignKey('juguete.id'))
    juguete_relacion = db.relationship('Juguete', backref="juguete")
