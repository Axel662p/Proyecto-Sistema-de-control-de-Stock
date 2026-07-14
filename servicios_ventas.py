"""Lógica de negocio para ventas"""
from database.productos import ProductosDB
from database.ventas import VentasDB

class ServiciosVentas:
    def __init__(self, db_productos, db_ventas, semaphore):
        self.db_productos = db_productos
        self.db_ventas = db_ventas
        self.semaphore = semaphore

    def procesar_venta(self, con, pid, cantidad, precio_unitario):
        """Procesar una venta de manera thread-safe"""

        try:
            cantidad = int(cantidad)
            assert cantidad > 0
        except Exception:
            return {
                "success": False,
                "error": "Cantidad inválida"
            }

        # Obtener producto
        producto = self.db_productos.obtener_por_id(con, pid)

        if not producto:
            return {
                "success": False,
                "error": "Producto no encontrado"
            }

        stock_disponible = producto[5]

        if cantidad > stock_disponible:
            return {
                "success": False,
                "error": f"Solo hay {stock_disponible} unidades"
            }

        # Calcular total
        total = cantidad * precio_unitario

        # Actualizar stock
        self.db_productos.actualizar_stock(con, pid, cantidad)

        # Registrar venta
        self.db_ventas.registrar_venta(con, pid, cantidad, total)

        return {
            "success": True,
            "total": total
        }

    def obtener_historial(self, con):
        """Obtener historial de ventas"""

        ventas = self.db_ventas.obtener_todas(con)
        resumen = self.db_ventas.obtener_resumen(con)

        return {
            "ventas": ventas,
            "num_ventas": resumen[0],
            "total_ingresos": resumen[1]
        }
