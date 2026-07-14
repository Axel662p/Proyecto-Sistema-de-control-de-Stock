"""Operaciones CRUD para ventas"""
from datetime import datetime
import threading

class VentasDB:
    def __init__(self, semaphore):
        self.semaphore = semaphore

    def registrar_venta(self, con, pid, cantidad, total):
        """Registrar una venta con thread-safety"""
        with self.semaphore:
            con.execute(
                "INSERT INTO ventas(fecha,producto_id,cantidad,total) VALUES(?,?,?,?)",
                (datetime.now().strftime("%Y-%m-%d %H:%M"), pid, cantidad, total)
            )
            con.commit()

    def obtener_todas(self, con):
        """Obtener todas las ventas con info del producto"""
        with self.semaphore:
            cur = con.execute("""
                SELECT v.fecha, p.nombre, v.cantidad, v.total
                FROM ventas v JOIN productos p ON p.id=v.producto_id
                ORDER BY v.id DESC""")
            return cur.fetchall()

    def obtener_resumen(self, con):
        """Obtener resumen de ventas (cantidad, total)"""
        with self.semaphore:
            cur = con.execute("""
                SELECT COUNT(*) as num_ventas, COALESCE(SUM(total), 0) as total_ingresos
                FROM ventas""")
            return cur.fetchone()
