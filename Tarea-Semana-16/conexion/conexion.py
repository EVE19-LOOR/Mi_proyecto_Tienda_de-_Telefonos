import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="quinende_celulares"
        )
        return conexion
    except Error as e:
        print("Error al conectar a MySQL:", e)
        return None