"""Vista de Historial de Ventas"""
import tkinter as tk
from tkinter import ttk

class VistaHistorial:
    def __init__(self, parent, servicios, app):
        self.parent = parent
        self.servicios = servicios
        self.app = app
        self._build()

    def _build(self):
        """Construir la interfaz de historial"""
        top = ttk.Frame(self.parent)
        top.pack(fill="x", padx=12, pady=10)
        self.lbl_resumen = ttk.Label(top, text="", font=("Segoe UI", 12, "bold"))
        self.lbl_resumen.pack(side="left")
        ttk.Button(top, text="🔄 Refrescar", command=self.cargar_historial).pack(side="right")

        cols = ("fecha", "producto", "cant", "total")
        self.tree_h = ttk.Treeview(self.parent, columns=cols, show="headings")
        for c, w in zip(cols, (160, 360, 100, 120)):
            self.tree_h.heading(c, text=c.capitalize())
            self.tree_h.column(c, width=w, anchor="center")
        self.tree_h.pack(fill="both", expand=True, padx=12, pady=10)

    def cargar_historial(self):
        """Cargar historial de ventas"""
        for r in self.tree_h.get_children():
            self.tree_h.delete(r)
        
        resultado = self.servicios.obtener_historial(self.app.con)
        ventas = resultado["ventas"]
        
        for row in ventas:
            self.tree_h.insert("", "end",
                               values=(row[0], row[1], row[2], f"${row[3]:,.2f}"))
        
        self.lbl_resumen.config(
            text=f"Ventas: {resultado['num_ventas']}   ·   Ingresos totales: ${resultado['total_ingresos']:,.2f}")
