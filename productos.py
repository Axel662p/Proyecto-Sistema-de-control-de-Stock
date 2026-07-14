"""Operaciones CRUD para productos"""
import sqlite3
import threading

class ProductosDB:
    def __init__(self, semaphore):
        self.semaphore = semaphore

    def agregar(self, con, datos):
        """Agregar nuevo producto con thread-safety"""
        with self.semaphore:
            try:
                con.execute(
                    "INSERT INTO productos(codigo,nombre,categoria,precio,stock) VALUES(?,?,?,?,?)",
                    datos
                )
                con.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def obtener_todos(self, con):
        """Obtener todos los productos"""
        with self.semaphore:
            cur = con.execute("SELECT * FROM productos ORDER BY nombre")
            return cur.fetchall()

    def obtener_por_id(self, con, pid):
        """Obtener producto por ID"""
        with self.semaphore:
            cur = con.execute("SELECT * FROM productos WHERE id=?", (pid,))
            return cur.fetchone()

    def actualizar(self, con, pid, datos):
        """Actualizar producto"""
        with self.semaphore:
            con.execute(
                "UPDATE productos SET codigo=?,nombre=?,categoria=?,precio=?,stock=? WHERE id=?",
                (*datos, pid)
            )
            con.commit()

    def eliminar(self, con, pid):
        """Eliminar producto"""
        with self.semaphore:
            con.execute("DELETE FROM productos WHERE id=?", (pid,))
            con.commit()

    def actualizar_stock(self, con, pid, cantidad):
        """Decrementar stock (para ventas)"""
        with self.semaphore:
            con.execute("UPDATE productos SET stock=stock-? WHERE id=?", (cantidad, pid))
            con.commit()
