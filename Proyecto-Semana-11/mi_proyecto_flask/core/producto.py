class Producto:
    def __init__(self, nombre, marca, modelo, categoria, cantidad, precio):
        self.nombre = (nombre or "").strip()
        self.marca = (marca or "").strip()
        self.modelo = (modelo or "").strip()
        self.categoria = (categoria or "").strip()
        self.cantidad = int(cantidad)
        self.precio = float(precio)

    def validar(self):
        if not self.nombre:
            raise ValueError("nombre vacío")
        if not self.marca:
            raise ValueError("marca vacía")
        if not self.modelo:
            raise ValueError("modelo vacío")
        if not self.categoria:
            raise ValueError("categoría vacía")
        if self.cantidad < 0:
            raise ValueError("cantidad negativa")
        if self.precio < 0:
            raise ValueError("precio negativo")