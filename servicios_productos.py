"""Lógica de negocio para productos"""
from database.productos import ProductosDB

class ServiciosProductos:
    def __init__(self, db_productos, semaphore):
        self.db = db_productos
        self.semaphore = semaphore

    def obtener_todos(self, con):
        """Obtener lista de productos para combobox"""
        return self.db.obtener_todos(con)

    def registrar_producto(self, con, codigo, nombre, categoria, precio, stock):
        """Registrar nuevo producto con validación"""
        if not codigo or not nombre:
            return {"success": False, "error": "Código y Nombre son obligatorios"}
        
        try:
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            return {"success": False, "error": "Precio debe ser número y Stock entero"}
        
        if precio < 0 or stock < 0:
            return {"success": False, "error": "Precio y Stock no pueden ser negativos"}
        
        datos = (codigo, nombre, categoria, precio, stock)
        if self.db.agregar(con, datos):
            return {"success": True}
        else:
            return {"success": False, "error": "Ese código ya existe"}

    def actualizar_producto(self, con, pid, codigo, nombre, categoria, precio, stock):
        """Actualizar producto existente"""
        try:
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            return {"success": False, "error": "Precio debe ser número y Stock entero"}
        
        datos = (codigo, nombre, categoria, precio, stock)
        self.db.actualizar(con, pid, datos)
        return {"success": True}

    def eliminar_producto(self, con, pid):
        """Eliminar producto"""
        self.db.eliminar(con, pid)
        return {"success": True}

    def calcular_inventario(self, con):
        """Calcular total de stock e inventario"""
        productos = self.db.obtener_todos(con)
        total_items = sum(p[5] for p in productos)
        total_valor = sum(p[5] * p[4] for p in productos)
        return {"total_items": total_items, "total_valor": total_valor}
