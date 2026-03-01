from core.db import get_conn

class Inventario:
    def __init__(self):
        self._items = {}        # diccionario: id -> producto
        self._categorias = set()  # conjunto: categorías únicas

    def cargar(self):
        self._items.clear()
        self._categorias.clear()

        conn = get_conn()
        rows = conn.execute("SELECT * FROM productos ORDER BY id DESC").fetchall()
        conn.close()

        for r in rows:
            self._items[r["id"]] = dict(r)
            self._categorias.add(r["categoria"])

    def listar(self):
        # lista para mostrar en tabla
        return list(self._items.values())

    def buscar(self, q):
        q = (q or "").strip().lower()
        if not q:
            return self.listar()
        return [p for p in self._items.values() if q in p["nombre"].lower()]

    def categorias(self):
        return set(self._categorias)

    def resumen(self):
        # tupla: (total_productos, total_unidades)
        total_productos = len(self._items)
        total_unidades = sum(int(p["cantidad"]) for p in self._items.values())
        return (total_productos, total_unidades)

    def agregar(self, producto):
        producto.validar()
        conn = get_conn()
        cur = conn.execute(
            "INSERT INTO productos(nombre,marca,modelo,categoria,cantidad,precio) VALUES (?,?,?,?,?,?)",
            (producto.nombre, producto.marca, producto.modelo, producto.categoria, producto.cantidad, producto.precio)
        )
        conn.commit()
        conn.close()
        return cur.lastrowid

    def obtener(self, pid):
        return self._items.get(pid)

    def actualizar(self, pid, producto):
        producto.validar()
        conn = get_conn()
        conn.execute(
            """UPDATE productos
               SET nombre=?, marca=?, modelo=?, categoria=?, cantidad=?, precio=?
               WHERE id=?""",
            (producto.nombre, producto.marca, producto.modelo, producto.categoria, producto.cantidad, producto.precio, pid)
        )
        conn.commit()
        conn.close()

    def eliminar(self, pid):
        conn = get_conn()
        conn.execute("DELETE FROM productos WHERE id=?", (pid,))
        conn.commit()
        conn.close()