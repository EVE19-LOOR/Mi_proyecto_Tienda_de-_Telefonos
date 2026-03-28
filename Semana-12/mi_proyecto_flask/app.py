from flask import Flask, render_template, request, redirect, url_for

from inventario.bd import db
from inventario.productos import Producto
from inventario.inventario import (
    guardar_txt,
    guardar_json,
    guardar_csv,
    leer_txt,
    leer_json,
    leer_csv,
)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///inventario.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/producto/nuevo", methods=["GET", "POST"])
def nuevo_producto():

    if request.method == "POST":

        nombre = request.form["nombre"]
        marca = request.form["marca"]
        precio = float(request.form["precio"])
        cantidad = int(request.form["cantidad"])

        producto = {
            "nombre": nombre,
            "marca": marca,
            "precio": precio,
            "cantidad": cantidad,
        }

        guardar_txt(producto)
        guardar_json(producto)
        guardar_csv(producto)

        nuevo = Producto(
            nombre=nombre,
            marca=marca,
            precio=precio,
            cantidad=cantidad,
        )

        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for("ver_datos"))

    return render_template("formulario.html")


@app.route("/datos")
def ver_datos():

    txt = leer_txt()
    json_d = leer_json()
    csv_d = leer_csv()
    db_d = Producto.query.all()

    return render_template(
        "datos.html",
        datos_txt=txt,
        datos_json=json_d,
        datos_csv=csv_d,
        datos_db=db_d,
    )


if __name__ == "__main__":
    app.run(debug=True)