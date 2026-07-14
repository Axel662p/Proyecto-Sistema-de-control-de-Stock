"""Vista de Ventas"""
import tkinter as tk
from tkinter import ttk, messagebox

class VistaVentas:
    def __init__(self, parent, servicios_prod, servicios_venta, app):
        self.parent = parent
        self.servicios_prod = servicios_prod
        self.servicios_venta = servicios_venta
        self.app = app
        self.prods = []
        self._build()

    def _build(self):
        """Construir la interfaz de ventas"""
        box = ttk.Frame(self.parent)
        box.pack(pady=40)

        ttk.Label(box, text="Producto", font=("Segoe UI", 11, "bold")).grid(
            row=0, column=0, sticky="w", pady=6)

        self.cmb = ttk.Combobox(box, width=40, state="readonly")
        self.cmb.grid(row=0, column=1, padx=10)
        self.cmb.bind("<<ComboboxSelected>>", self._info_prod)

        ttk.Label(box, text="Cantidad", font=("Segoe UI", 11, "bold")).grid(
            row=1, column=0, sticky="w", pady=6)

        self.ent_cant = ttk.Entry(box, width=12)
        self.ent_cant.grid(row=1, column=1, sticky="w", padx=10)
        self.ent_cant.bind("<KeyRelease>", self._calc_total)

        self.lbl_info = ttk.Label(
            box,
            text="",
            font=("Segoe UI", 10, "italic")
        )
        self.lbl_info.grid(row=2, column=0, columnspan=2, pady=10)

        self.lbl_tot = tk.Label(
            box,
            text="Total: $0.00",
            bg="#0f172a",
            fg="#10b981",
            font=("Segoe UI", 22, "bold")
        )
        self.lbl_tot.grid(row=3, column=0, columnspan=2, pady=20)

        ttk.Button(
            box,
            text="💵 Registrar Venta",
            style="Ok.TButton",
            command=self.vender
        ).grid(
            row=4,
            column=0,
            columnspan=2,
            pady=10,
            ipadx=20
        )

    def cargar_combo(self):
        """Cargar productos en combo"""
        self.prods = self.servicios_prod.obtener_todos(self.app.con)

        # nombre - código
        self.cmb["values"] = [
            f"{p[2]} - {p[1]}"
            for p in self.prods
        ]

        self.cmb.set("")
        self.lbl_info.config(text="")
        self.lbl_tot.config(text="Total: $0.00")

    def _prod_actual(self):
        """Obtener producto seleccionado"""
        i = self.cmb.current()
        return self.prods[i] if i >= 0 else None

    def _info_prod(self, _=None):
        """Mostrar información del producto"""
        p = self._prod_actual()

        if p:
            # p[4] = precio
            # p[5] = stock
            self.lbl_info.config(
                text=f"Precio: ${p[4]:.2f}   ·   Stock disponible: {p[5]}"
            )

            self._calc_total()

    def _calc_total(self, _=None):
        """Calcular total"""
        p = self._prod_actual()

        if not p:
            self.lbl_tot.config(text="Total: $0.00")
            return

        try:
            cantidad = int(self.ent_cant.get())

            if cantidad <= 0:
                raise ValueError

            total = p[4] * cantidad

            self.lbl_tot.config(
                text=f"Total: ${total:,.2f}"
            )

        except (ValueError, TypeError):
            self.lbl_tot.config(text="Total: $0.00")

    def vender(self):
        """Procesar venta"""
        p = self._prod_actual()

        if not p:
            messagebox.showwarning(
                "Falta",
                "Selecciona un producto."
            )
            return

        try:
            cantidad = int(self.ent_cant.get())

            if cantidad <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Error",
                "Cantidad inválida."
            )
            return

        # p[0] = id
        # p[4] = precio
        resultado = self.servicios_venta.procesar_venta(
            self.app.con,
            p[0],
            cantidad,
            p[4]
        )

        if resultado["success"]:

            messagebox.showinfo(
                "Venta OK",
                f"Venta registrada por ${resultado['total']:,.2f}"
            )

            self.ent_cant.delete(0, "end")

            self.app.reload_productos()
            self.cargar_combo()
            self.app.reload_historial()

        else:

            messagebox.showerror(
                "Error",
                resultado["error"]
            )
