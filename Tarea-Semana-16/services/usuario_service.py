from conexion.conexion import obtener_conexion

def registrar_usuario(nombre, usuario, clave):
    conexion = obtener_conexion()
    if conexion is None:
        return False, "No se pudo conectar con la base de datos"

    try:
        cursor = conexion.cursor()
        sql = """
        INSERT INTO usuarios (nombre, usuario, clave)
        VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (nombre, usuario, clave))
        conexion.commit()
        return True, "Usuario registrado correctamente"
    except Exception as e:
        conexion.rollback()
        return False, f"Error al registrar usuario: {e}"
    finally:
        cursor.close()
        conexion.close()


def validar_usuario(usuario, clave):
    conexion = obtener_conexion()
    if conexion is None:
        return None

    try:
        cursor = conexion.cursor(dictionary=True)
        sql = """
        SELECT * FROM usuarios
        WHERE usuario = %s AND clave = %s
        """
        cursor.execute(sql, (usuario, clave))
        return cursor.fetchone()
    except Exception as e:
        print("Error al validar usuario:", e)
        return None
    finally:
        cursor.close()
        conexion.close()