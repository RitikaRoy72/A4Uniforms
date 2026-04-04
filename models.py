from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Cadet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cadet_id = db.Column(db.String, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    rank = db.Column(db.String)
    flight = db.Column(db.String)
    password_hash = db.Column(db.String, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)


class UniformType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    category = db.Column(db.String)  # Blues / OCP / PTG


class IssuedUniform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cadet_id = db.Column(db.Integer, db.ForeignKey("cadet.id"))
    uniform_type_id = db.Column(db.Integer, db.ForeignKey("uniform_type.id"))
    size = db.Column(db.String)
    qty = db.Column(db.Integer, default=1)


class SupplyInventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uniform_type_id = db.Column(db.Integer, db.ForeignKey("uniform_type.id"))
    size = db.Column(db.String)
    quantity = db.Column(db.Integer)


class UniformRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cadet_id = db.Column(db.Integer, db.ForeignKey("cadet.id"))
    uniform_item = db.Column(db.String)
    size = db.Column(db.String)
    reason = db.Column(db.String)
    status = db.Column(db.String, default="PENDING")
