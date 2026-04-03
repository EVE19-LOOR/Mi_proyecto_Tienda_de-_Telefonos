from conexion.conexion import obtener_conexion

def validar_usuario(correo, clave):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    sql = "SELECT * FROM usuarios WHERE correo = %s AND clave = %s"
    cursor.execute(sql, (correo, clave))
    usuario = cursor.fetchone()

    cursor.close()
    conexion.close()

    return usuario


def existe_correo(correo):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    sql = "SELECT * FROM usuarios WHERE correo = %s"
    cursor.execute(sql, (correo,))
    usuario = cursor.fetchone()

    cursor.close()
    conexion.close()

    return usuario


def registrar_usuario(nombre, correo, clave):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    sql = "INSERT INTO usuarios (nombre, correo, clave) VALUES (%s, %s, %s)"
    cursor.execute(sql, (nombre, correo, clave))

    conexion.commit()
    cursor.close()
    conexion.close()