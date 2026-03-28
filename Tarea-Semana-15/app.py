from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from services.producto_service import (
    listar_productos,
    obtener_producto_por_id,
    insertar_producto,
    actualizar_producto,
    eliminar_producto
)
from forms.producto_form import ProductoForm
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = "clave_secreta_tienda"

@app.route("/")
def inicio():
    return redirect(url_for("listar_productos_route"))

@app.route("/productos")
def listar_productos_route():
    productos = listar_productos()
    return render_template("productos/listar.html", productos=productos)

@app.route("/productos/crear", methods=["GET", "POST"])
def crear_producto_route():
    if request.method == "POST":
        nombre = request.form["nombre"]
        marca = request.form["marca"]
        precio = request.form["precio"]
        stock = request.form["stock"]

        errores = ProductoForm.validar(nombre, marca, precio, stock)

        if errores:
            for error in errores:
                flash(error, "danger")
            return render_template("productos/crear.html")

        insertar_producto(nombre, marca, precio, stock)
        flash("Producto registrado correctamente.", "success")
        return redirect(url_for("listar_productos_route"))

    return render_template("productos/crear.html")

@app.route("/productos/editar/<int:id_producto>", methods=["GET", "POST"])
def editar_producto_route(id_producto):
    producto = obtener_producto_por_id(id_producto)

    if not producto:
        flash("Producto no encontrado.", "danger")
        return redirect(url_for("listar_productos_route"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        marca = request.form["marca"]
        precio = request.form["precio"]
        stock = request.form["stock"]

        errores = ProductoForm.validar(nombre, marca, precio, stock)

        if errores:
            for error in errores:
                flash(error, "danger")
            return render_template("productos/editar.html", producto=producto)

        actualizar_producto(id_producto, nombre, marca, precio, stock)
        flash("Producto actualizado correctamente.", "warning")
        return redirect(url_for("listar_productos_route"))

    return render_template("productos/editar.html", producto=producto)

@app.route("/productos/eliminar/<int:id_producto>", methods=["GET", "POST"])
def eliminar_producto_route(id_producto):
    producto = obtener_producto_por_id(id_producto)

    if not producto:
        flash("Producto no encontrado.", "danger")
        return redirect(url_for("listar_productos_route"))

    if request.method == "POST":
        eliminar_producto(id_producto)
        flash("Producto eliminado correctamente.", "secondary")
        return redirect(url_for("listar_productos_route"))

    return render_template("productos/eliminar.html", producto=producto)

@app.route("/productos/pdf")
def generar_pdf_productos():
    productos = listar_productos()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(190, 10, "Reporte de celulares en tienda", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "B", 10)
    pdf.cell(20, 10, "ID", 1)
    pdf.cell(50, 10, "Nombre", 1)
    pdf.cell(40, 10, "Marca", 1)
    pdf.cell(40, 10, "Precio", 1)
    pdf.cell(40, 10, "Stock", 1)
    pdf.ln()

    pdf.set_font("Arial", "", 10)
    for producto in productos:
        pdf.cell(20, 10, str(producto["id_producto"]), 1)
        pdf.cell(50, 10, str(producto["nombre"]), 1)
        pdf.cell(40, 10, str(producto["marca"]), 1)
        pdf.cell(40, 10, str(producto["precio"]), 1)
        pdf.cell(40, 10, str(producto["stock"]), 1)
        pdf.ln()

    nombre_archivo = "reporte_celulares.pdf"
    pdf.output(nombre_archivo)

    return send_file(nombre_archivo, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)