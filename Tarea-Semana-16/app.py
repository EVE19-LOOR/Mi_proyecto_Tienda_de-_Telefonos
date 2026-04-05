from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from services.producto_service import (
    obtener_productos,
    obtener_producto_por_id,
    agregar_producto,
    actualizar_producto,
    eliminar_producto
)
from services.usuario_service import registrar_usuario, validar_usuario
from services.compra_service import registrar_compra, obtener_compra_por_id, obtener_compras
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)
app.secret_key = "clave_secreta_quinende"


@app.route('/')
def inicio():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']

        usuario_bd = validar_usuario(usuario, clave)

        if usuario_bd:
            session['usuario'] = usuario_bd['usuario']
            session['id_usuario'] = usuario_bd['id_usuario']
            session['nombre'] = usuario_bd['nombre']
            return redirect(url_for('listar_productos'))
        else:
            flash('Usuario o contraseña incorrectos')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        usuario = request.form['usuario']
        clave = request.form['clave']

        exito, mensaje = registrar_usuario(nombre, usuario, clave)
        flash(mensaje)

        if exito:
            return redirect(url_for('login'))
        return redirect(url_for('registro'))

    return render_template('registro.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/productos')
def listar_productos():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    busqueda = request.args.get('q', '')
    productos = obtener_productos(busqueda)
    return render_template('productos/listar.html', productos=productos, busqueda=busqueda)


@app.route('/productos/crear', methods=['GET', 'POST'])
def crear_producto():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        marca = request.form['marca']
        precio = request.form['precio']
        stock = request.form['stock']

        exito, mensaje = agregar_producto(nombre, marca, precio, stock)
        flash(mensaje)

        if exito:
            return redirect(url_for('listar_productos'))
        return redirect(url_for('crear_producto'))

    return render_template('productos/crear.html')


@app.route('/productos/editar/<int:id_producto>', methods=['GET', 'POST'])
def editar_producto(id_producto):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    producto = obtener_producto_por_id(id_producto)

    if not producto:
        flash('Celular no encontrado')
        return redirect(url_for('listar_productos'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        marca = request.form['marca']
        precio = request.form['precio']
        stock = request.form['stock']

        exito, mensaje = actualizar_producto(id_producto, nombre, marca, precio, stock)
        flash(mensaje)

        if exito:
            return redirect(url_for('listar_productos'))
        return redirect(url_for('editar_producto', id_producto=id_producto))

    return render_template('productos/editar.html', producto=producto)


@app.route('/productos/eliminar/<int:id_producto>')
def borrar_producto(id_producto):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    exito, mensaje = eliminar_producto(id_producto)
    flash(mensaje)
    return redirect(url_for('listar_productos'))


@app.route('/comprar/<int:id_producto>', methods=['GET', 'POST'])
def comprar_producto(id_producto):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    producto = obtener_producto_por_id(id_producto)

    if not producto:
        flash('Celular no encontrado')
        return redirect(url_for('listar_productos'))

    if request.method == 'POST':
        cantidad = int(request.form['cantidad'])
        id_usuario = session['id_usuario']

        exito, mensaje, id_compra = registrar_compra(id_usuario, id_producto, cantidad)
        flash(mensaje)

        if exito:
            return redirect(url_for('generar_pdf_compra', id_compra=id_compra))
        return redirect(url_for('comprar_producto', id_producto=id_producto))

    return render_template('productos/comprar.html', producto=producto)


@app.route('/compras')
def listar_compras():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    compras = obtener_compras()
    return render_template('productos/compras.html', compras=compras)


@app.route('/compra/pdf/<int:id_compra>')
def generar_pdf_compra(id_compra):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    compra = obtener_compra_por_id(id_compra)

    if not compra:
        flash('Compra no encontrada')
        return redirect(url_for('listar_productos'))

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle("Factura_Quinende_Celulares")

    pdf.rect(40, 430, 530, 340)

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(180, 740, "Quinende Celulares")

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, 710, "Reporte de compra")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 680, f"Factura N°: {compra['id_compra']}")
    pdf.drawString(50, 660, f"Cliente: {compra['cliente']}")
    pdf.drawString(50, 640, f"Usuario comprador: {compra['usuario']}")
    pdf.drawString(50, 620, f"Celular: {compra['producto']}")
    pdf.drawString(50, 600, f"Marca: {compra['marca']}")
    pdf.drawString(50, 580, f"Cantidad comprada: {compra['cantidad']}")
    pdf.drawString(50, 560, f"Precio unitario: ${compra['precio']}")
    pdf.drawString(50, 540, f"Total cancelado: ${compra['total']}")
    pdf.drawString(50, 520, f"Fecha de compra: {compra['fecha']}")

    pdf.line(50, 500, 540, 500)
    pdf.drawString(50, 475, "Documento generado por el sistema Quinende Celulares.")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=factura_{id_compra}.pdf'
    return response


if __name__ == '__main__':
    app.run(debug=True)