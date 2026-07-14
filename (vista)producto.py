"""Vista de Productos"""
import tkinter as tk
from tkinter import ttk, messagebox

class VistaProductos:
    def __init__(self, parent, servicios, app):
        self.parent = parent
        self.servicios = servicios
        self.app = app  # Referencia a la app principal
        self.selected_id = None
        self._build()

    def _build(self):
        """Construir la interfaz de productos"""
        # Frame de formulario
        form = ttk.Frame(self.parent)
        form.pack(fill="x", padx=12, pady=12)

        labels = ["Código", "Nombre", "Categoría", "Precio", "Stock"]
        self.entries = {}
        for i, l in enumerate(labels):
            ttk.Label(form, text=l).grid(row=0, column=i, padx=6, sticky="w")
            e = ttk.Entry(form, width=18)
            e.grid(row=1, column=i, padx=6, ipady=4)
            self.entries[l] = e

        # Frame de botones
        btns = ttk.Frame(self.parent)
        btns.pack(fill="x", padx=12)
        ttk.Button(btns, text="➕ Agregar", style="Ok.TButton",
                   command=self.agregar).pack(side="left", padx=4)
        ttk.Button(btns, text="✏️ Actualizar",
                   command=self.actualizar).pack(side="left", padx=4)
        ttk.Button(btns, text="🗑 Eliminar", style="Danger.TButton",
                   command=self.eliminar).pack(side="left", padx=4)
        ttk.Button(btns, text="🧹 Limpiar",
                   command=self.limpiar).pack(side="left", padx=4)

        # Treeview
        cols = ("id", "codigo", "nombre", "categoria", "precio", "stock")
        self.tree = ttk.Treeview(self.parent, columns=cols, show="headings")
        for c, w in zip(cols, (50, 110, 240, 150, 110, 90)):
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=w, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=12, pady=12)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar)

    def cargar_productos(self):
        """Cargar datos en la tabla"""
        for r in self.tree.get_children():
            self.tree.delete(r)
        
        productos = self.servicios.obtener_todos(self.app.con)
        for row in productos:
            self.tree.insert("", "end", values=row,
                             tags=("low",) if row[5] < 5 else ())
        
        self.tree.tag_configure("low", background="#7f1d1d", foreground="white")
        
        # Actualizar totales
        inv = self.servicios.calcular_inventario(self.app.con)
        self.app.lbl_total.config(
            text=f"Stock total: {inv['total_items']} uds · Valor: ${inv['total_valor']:,.2f}")

    def _get_form_data(self):
        """Obtener datos del formulario"""
        try:
            return (
                self.entries["Código"].get().strip(),
                self.entries["Nombre"].get().strip(),
                self.entries["Categoría"].get().strip(),
                float(self.entries["Precio"].get()),
                int(self.entries["Stock"].get()),
            )
        except ValueError:
            messagebox.showerror("Error", "Precio debe ser número y Stock entero.")
            return None

    def agregar(self):
        """Agregar producto"""
        d = self._get_form_data()
        if not d:
            return
        
        resultado = self.servicios.registrar_producto(
            self.app.con, d[0], d[1], d[2], d[3], d[4])
        
        if resultado["success"]:
            self.cargar_productos()
            self.app.reload_venta_combo()
            self.limpiar()
        else:
            messagebox.showerror("Error", resultado["error"])

    def seleccionar(self, _):
        """Seleccionar producto de la tabla"""
        sel = self.tree.selection()
        if not sel:
            return
        v = self.tree.item(sel[0])["values"]
        self.selected_id = v[0]
        for k, val in zip(["Código", "Nombre", "Categoría", "Precio", "Stock"], v[1:]):
            self.entries[k].delete(0, "end")
            self.entries[k].insert(0, val)

    def actualizar(self):
        """Actualizar producto"""
        if not self.selected_id:
            messagebox.showinfo("Selecciona", "Elige un producto de la lista.")
            return
        
        d = self._get_form_data()
        if not d:
            return
        
        resultado = self.servicios.actualizar_producto(
            self.app.con, self.selected_id, d[0], d[1], d[2], d[3], d[4])
        
        if resultado["success"]:
            self.cargar_productos()
            self.app.reload_venta_combo()
            self.limpiar()
        else:
            messagebox.showerror("Error", resultado["error"])

    def eliminar(self):
        """Eliminar producto"""
        if not self.selected_id:
            messagebox.showinfo("Selecciona", "Elige un producto de la lista.")
            return
        
        if messagebox.askyesno("Confirmar", "¿Eliminar producto?"):
            resultado = self.servicios.eliminar_producto(self.app.con, self.selected_id)
            if resultado["success"]:
                self.cargar_productos()
                self.app.reload_venta_combo()
                self.limpiar()
                self.selected_id = None

    def limpiar(self):
        """Limpiar formulario"""
        for e in self.entries.values():
            e.delete(0, "end")
        self.selected_id = None
