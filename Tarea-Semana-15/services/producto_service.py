from conexion.conexion import obtener_conexion

def listar_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos ORDER BY id_producto DESC")
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return productos

def obtener_producto_por_id(id_producto):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
    producto = cursor.fetchone()
    cursor.close()
    conexion.close()
    return producto

def insertar_producto(nombre, marca, precio, stock):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sql = "INSERT INTO productos (nombre, marca, precio, stock) VALUES (%s, %s, %s, %s)"
    valores = (nombre, marca, precio, stock)
    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()

def actualizar_producto(id_producto, nombre, marca, precio, stock):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sql = """
        UPDATE productos
        SET nombre = %s, marca = %s, precio = %s, stock = %s
        WHERE id_producto = %s
    """
    valores = (nombre, marca, precio, stock, id_producto)
    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()

def eliminar_producto(id_producto):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
    conexion.commit()
    cursor.close()
    conexion.close()