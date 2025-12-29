from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cadet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cadet_id = db.Column(db.String, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    rank = db.Column(db.String)
    flight = db.Column(db.String)


class UniformType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    category = db.Column(db.String)  # Blues / OCP / PTG



class IssuedUniform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cadet_id = db.Column(db.Integer, db.ForeignKey("cadet.id"))
    uniform_type_id = db.Column(db.Integer, db.ForeignKey("uniform_type.id"))
    size = db.Column(db.String)


class SupplyInventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uniform_type_id = db.Column(db.Integer, db.ForeignKey("uniform_type.id"))
    size = db.Column(db.String)
    quantity = db.Column(db.Integer)


class UniformRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cadet_id = db.Column(db.Integer, db.ForeignKey("cadet.id"))
