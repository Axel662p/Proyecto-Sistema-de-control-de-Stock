"""
Sistema de Tienda / Gestión de Stock - MODULARIZADO CON THREADING Y ASYNCIO
Interfaz gráfica con Tkinter + SQLite + Semáforos + Asyncio.
"""

import tkinter as tk
from tkinter import ttk
import threading
import asyncio

# Importar módulos de base de datos
from database.conexion import database
from database.productos import ProductosDB
from database.ventas import VentasDB

# Importar servicios
from servicios.servicios_productos import ServiciosProductos
from servicios.servicios_ventas import ServiciosVentas

# Importar vistas
from ui.estilos import estilos
from ui.vistas.productos import VistaProductos
from ui.vistas.ventas import VistaVentas
from ui.vistas.historial import VistaHistorial


class TiendaApp(tk.Tk):
    """Aplicación principal de gestión de tienda con threading y asyncio"""

    def __init__(self):
        super().__init__()

        self.title("Sistema de Tienda - Gestión de Stock")
        self.geometry("1000x620")
        self.configure(bg="#0f172a")

        # ===== SEMÁFORO =====
        self.db_semaphore = threading.Semaphore(1)

        # ===== BASE DE DATOS =====
        self.con = database.conectar()

        # ===== CAPA DE DATOS =====
        self.db_productos = ProductosDB(self.db_semaphore)
        self.db_ventas = VentasDB(self.db_semaphore)

        # ===== SERVICIOS =====
        self.serv_productos = ServiciosProductos(
            self.db_productos,
            self.db_semaphore
        )

        self.serv_ventas = ServiciosVentas(
            self.db_productos,
            self.db_ventas,
            self.db_semaphore
        )

        # ===== UI =====
        estilos(self)
        self._build_ui()

        # ===== HILO PARA CARGA INICIAL =====
        threading.Thread(
            target=self._cargar_datos_iniciales,
            daemon=True
        ).start()

    def _build_ui(self):
        """Construir interfaz"""

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=14, pady=10)

        self.tab_prod = ttk.Frame(self.nb)
        self.tab_venta = ttk.Frame(self.nb)
        self.tab_hist = ttk.Frame(self.nb)

        self.nb.add(self.tab_prod, text="  📦 Productos  ")
        self.nb.add(self.tab_venta, text="  🛒 Vender  ")
        self.nb.add(self.tab_hist, text="  📊 Historial  ")

        self.vista_prod = VistaProductos(
            self.tab_prod,
            self.serv_productos,
            self
        )

        self.vista_venta = VistaVentas(
            self.tab_venta,
            self.serv_productos,
            self.serv_ventas,
            self
        )

        self.vista_hist = VistaHistorial(
            self.tab_hist,
            self.serv_ventas,
            self
        )

    # ===== ASYNCIO =====
    async def carga_async(self):
        """
        Simula una tarea asíncrona.
        Puede representar lectura de datos,
        sincronización o carga inicial.
        """
        await asyncio.sleep(1)

    def _cargar_datos_iniciales(self):
        """Carga inicial usando asyncio dentro de un hilo"""

        # Ejecutar coroutine
        asyncio.run(self.carga_async())

        # Actualizar GUI
        self.after(100, self.reload_productos)
        self.after(100, self.reload_venta_combo)
        self.after(100, self.reload_historial)

    def reload_productos(self):
        self.vista_prod.cargar_productos()

    def reload_venta_combo(self):
        self.vista_venta.cargar_combo()

    def reload_historial(self):
        self.vista_hist.cargar_historial()


if __name__ == "__main__":
    app = TiendaApp()
    app.mainloop()
