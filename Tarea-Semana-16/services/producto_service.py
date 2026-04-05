from conexion.conexion import obtener_conexion

def obtener_productos(busqueda=''):
    conexion = obtener_conexion()
    if conexion is None:
        return []

    try:
        cursor = conexion.cursor(dictionary=True)

        if busqueda:
            sql = """
            SELECT id_producto, nombre, marca, precio, stock
            FROM productos
            WHERE nombre LIKE %s OR marca LIKE %s
            ORDER BY id_producto DESC
            """
            dato = f"%{busqueda}%"
            cursor.execute(sql, (dato, dato))
        else:
            sql = """
            SELECT id_producto, nombre, marca, precio, stock
            FROM productos
            ORDER BY id_producto DESC
            """
            cursor.execute(sql)

        return cursor.fetchall()
    except Exception as e:
        print("Error al obtener productos:", e)
        return []
    finally:
        cursor.close()
        conexion.close()


def obtener_producto_por_id(id_producto):
    conexion = obtener_conexion()
    if conexion is None:
        return None

    try:
        cursor = conexion.cursor(dictionary=True)
        sql = """
        SELECT id_producto, nombre, marca, precio, stock
        FROM productos
        WHERE id_producto = %s
        """
        cursor.execute(sql, (id_producto,))
        return cursor.fetchone()
    except Exception as e:
        print("Error al obtener producto:", e)
        return None
    finally:
        cursor.close()
        conexion.close()


def agregar_producto(nombre, marca, precio, stock):
    conexion = obtener_conexion()
    if conexion is None:
        return False, "No se pudo conectar con la base de datos"

    try:
        cursor = conexion.cursor()
        sql = """
        INSERT INTO productos (nombre, marca, precio, stock)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (nombre, marca, precio, stock))
        conexion.commit()
        return True, "Celular agregado correctamente"
    except Exception as e:
        conexion.rollback()
        return False, f"Error al agregar celular: {e}"
    finally:
        cursor.close()
        conexion.close()


def actualizar_producto(id_producto, nombre, marca, precio, stock):
    conexion = obtener_conexion()
    if conexion is None:
        return False, "No se pudo conectar con la base de datos"

    try:
        cursor = conexion.cursor()
        sql = """
        UPDATE productos
        SET nombre = %s, marca = %s, precio = %s, stock = %s
        WHERE id_producto = %s
        """
        cursor.execute(sql, (nombre, marca, precio, stock, id_producto))
        conexion.commit()
        return True, "Celular actualizado correctamente"
    except Exception as e:
        conexion.rollback()
        return False, f"Error al actualizar celular: {e}"
    finally:
        cursor.close()
        conexion.close()


def eliminar_producto(id_producto):
    conexion = obtener_conexion()
    if conexion is None:
        return False, "No se pudo conectar con la base de datos"

    try:
        cursor = conexion.cursor()
        sql = "DELETE FROM productos WHERE id_producto = %s"
        cursor.execute(sql, (id_producto,))
        conexion.commit()
        return True, "Celular eliminado correctamente"
    except Exception as e:
        conexion.rollback()
        return False, f"Error al eliminar celular: {e}"
    finally:
        cursor.close()
        conexion.close()