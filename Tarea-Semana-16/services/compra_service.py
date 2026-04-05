from conexion.conexion import obtener_conexion

def registrar_compra(id_usuario, id_producto, cantidad):
    conexion = obtener_conexion()
    if conexion is None:
        return False, "No se pudo conectar con la base de datos", None

    try:
        cursor = conexion.cursor(dictionary=True)

        sql_producto = "SELECT * FROM productos WHERE id_producto = %s"
        cursor.execute(sql_producto, (id_producto,))
        producto = cursor.fetchone()

        if not producto:
            return False, "Celular no encontrado", None

        if int(producto["stock"]) <= 0:
            return False, "No hay stock disponible", None

        if int(cantidad) > int(producto["stock"]):
            return False, "La cantidad supera el stock disponible", None

        total = float(producto["precio"]) * int(cantidad)

        sql_compra = """
        INSERT INTO compras (id_usuario, id_producto, cantidad, total)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql_compra, (id_usuario, id_producto, cantidad, total))

        sql_stock = """
        UPDATE productos
        SET stock = stock - %s
        WHERE id_producto = %s
        """
        cursor.execute(sql_stock, (cantidad, id_producto))

        id_compra = cursor.lastrowid
        conexion.commit()

        return True, "Compra registrada correctamente", id_compra

    except Exception as e:
        conexion.rollback()
        return False, f"Error al registrar compra: {e}", None
    finally:
        cursor.close()
        conexion.close()


def obtener_compra_por_id(id_compra):
    conexion = obtener_conexion()
    if conexion is None:
        return None

    try:
        cursor = conexion.cursor(dictionary=True)
        sql = """
        SELECT c.id_compra, c.cantidad, c.total, c.fecha,
               u.nombre AS cliente,
               u.usuario,
               p.nombre AS producto,
               p.marca,
               p.precio
        FROM compras c
        INNER JOIN usuarios u ON c.id_usuario = u.id_usuario
        INNER JOIN productos p ON c.id_producto = p.id_producto
        WHERE c.id_compra = %s
        """
        cursor.execute(sql, (id_compra,))
        return cursor.fetchone()
    except Exception as e:
        print("Error al obtener compra:", e)
        return None
    finally:
        cursor.close()
        conexion.close()


def obtener_compras():
    conexion = obtener_conexion()
    if conexion is None:
        return []

    try:
        cursor = conexion.cursor(dictionary=True)
        sql = """
        SELECT c.id_compra, c.cantidad, c.total, c.fecha,
               u.nombre AS cliente,
               u.usuario,
               p.nombre AS producto,
               p.marca,
               p.precio
        FROM compras c
        INNER JOIN usuarios u ON c.id_usuario = u.id_usuario
        INNER JOIN productos p ON c.id_producto = p.id_producto
        ORDER BY c.id_compra DESC
        """
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print("Error al obtener compras:", e)
        return []
    finally:
        cursor.close()
        conexion.close()