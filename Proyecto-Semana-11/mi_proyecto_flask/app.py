from flask import Flask, render_template, request, redirect, url_for

from core.db import init_db
from core.inventario import Inventario
from core.producto import Producto

app = Flask(__name__)

# Crear base y tabla en localhost (archivo data/inventario.db)
init_db()

# Inventario (POO + colecciones)
inv = Inventario()

# Datos simulados del catálogo (se mantiene)
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
        return render_template(
            "resultado.html",
            cliente=cliente,
            telefono=telefono,
            cantidad=cantidad
        )
    return render_template("pedido.html")


# -------------------- INVENTARIO (CRUD + SQLite) --------------------

@app.get("/inventario")
def inventario_list():
    inv.cargar()
    q = request.args.get("q", "")
    productos = inv.buscar(q)
    resumen = inv.resumen()
    return render_template(
        "inventario/list.html",
        productos=productos,
        q=q,
        resumen=resumen
    )


@app.route("/inventario/nuevo", methods=["GET", "POST"])
def inventario_new():
    error = ""
    if request.method == "POST":
        try:
            p = Producto(
                request.form.get("nombre"),
                request.form.get("marca"),
                request.form.get("modelo"),
                request.form.get("categoria"),
                request.form.get("cantidad"),
                request.form.get("precio"),
            )
            inv.agregar(p)
            return redirect(url_for("inventario_list"))
        except Exception as e:
            error = str(e)

    return render_template("inventario/form.html", titulo="Nuevo producto", p=None, error=error)


@app.route("/inventario/<int:pid>/editar", methods=["GET", "POST"])
def inventario_edit(pid: int):
    inv.cargar()
    actual = inv.obtener(pid)
    if not actual:
        return redirect(url_for("inventario_list"))

    error = ""
    if request.method == "POST":
        try:
            nuevo = Producto(
                request.form.get("nombre"),
                request.form.get("marca"),
                request.form.get("modelo"),
                request.form.get("categoria"),
                request.form.get("cantidad"),
                request.form.get("precio"),
            )
            inv.actualizar(pid, nuevo)
            return redirect(url_for("inventario_list"))
        except Exception as e:
            error = str(e)

    # "actual" es dict, se pasa como objeto simple a la vista
    class Obj:
        pass
    p = Obj()
    p.nombre = actual["nombre"]
    p.marca = actual["marca"]
    p.modelo = actual["modelo"]
    p.categoria = actual["categoria"]
    p.cantidad = actual["cantidad"]
    p.precio = actual["precio"]

    return render_template("inventario/form.html", titulo="Editar producto", p=p, error=error)


@app.post("/inventario/<int:pid>/eliminar")
def inventario_delete(pid: int):
    inv.eliminar(pid)
    return redirect(url_for("inventario_list"))


if __name__ == "__main__":
    app.run(debug=True)