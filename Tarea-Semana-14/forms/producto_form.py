class ProductoForm:
    @staticmethod
    def validar(nombre, marca, precio, stock):
        errores = []

        if not nombre or nombre.strip() == "":
            errores.append("El nombre del celular es obligatorio.")

        if not marca or marca.strip() == "":
            errores.append("La marca es obligatoria.")

        try:
            precio = float(precio)
            if precio < 0:
                errores.append("El precio no puede ser negativo.")
        except ValueError:
            errores.append("El precio debe ser numérico.")

        try:
            stock = int(stock)
            if stock < 0:
                errores.append("El stock no puede ser negativo.")
        except ValueError:
            errores.append("El stock debe ser un número entero.")

        return errores