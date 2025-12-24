from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///uniforms.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -------- MODEL --------
class UniformItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_type = db.Column(db.String(50))
    size = db.Column(db.String(20))
    condition = db.Column(db.String(20))
    status = db.Column(db.String(20))


# -------- ROUTES --------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inventory")
def inventory():
    items = UniformItem.query.all()
    return render_template("inventory.html", items=items)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()   
    app.run(debug=True)
