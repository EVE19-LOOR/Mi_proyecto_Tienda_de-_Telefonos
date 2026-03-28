class Producto:
    def __init__(self, id_producto=None, nombre="", marca="", precio=0.0, stock=0):
        self.id_producto = id_producto
        self.nombre = nombre
        self.marca = marca
        self.precio = precio
        self.stock = stock