from flask import Flask, render_template, request

app = Flask(__name__)

# Datos simulados
telefonos = [
    {"marca": "Apple", "modelo": "iPhone 13", "precio": 699},
    {"marca": "Samsung", "modelo": "Galaxy S23", "precio": 799},
    {"marca": "Xiaomi", "modelo": "Redmi Note 13", "precio": 249}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/catalogo")
def catalogo():
    return render_template("catalogo.html", telefonos=telefonos)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/pedido", methods=["GET", "POST"])
def pedido():
    if request.method == "POST":
        cliente = request.form.get("cliente")
        telefono = request.form.get("telefono")
        cantidad = request.form.get("cantidad")
        return render_template("resultado.html",
                               cliente=cliente,
                               telefono=telefono,
                               cantidad=cantidad)
    return render_template("pedido.html")


if __name__ == "__main__":
    app.run(debug=True)
