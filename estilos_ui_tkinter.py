"""Estilos y configuración de UI con Tkinter"""
import tkinter as tk
from tkinter import ttk

def estilos(root):
    """Aplicar estilos al widget root"""
    s = ttk.Style()
    s.theme_use("clam")
    bg, fg, acc = "#0f172a", "#e2e8f0", "#6366f1"
    
    s.configure("TNotebook", background=bg, borderwidth=0)
    s.configure("TNotebook.Tab", background="#1e293b", foreground=fg,
                padding=[18, 10], font=("Segoe UI", 10, "bold"))
    s.map("TNotebook.Tab", background=[("selected", acc)],
          foreground=[("selected", "white")])
    s.configure("TFrame", background=bg)
    s.configure("TLabel", background=bg, foreground=fg, font=("Segoe UI", 10))
    s.configure("TButton", background=acc, foreground="white",
                font=("Segoe UI", 10, "bold"), padding=8, borderwidth=0)
    s.map("TButton", background=[("active", "#4f46e5")])
    s.configure("Danger.TButton", background="#ef4444")
    s.map("Danger.TButton", background=[("active", "#dc2626")])
    s.configure("Ok.TButton", background="#10b981")
    s.map("Ok.TButton", background=[("active", "#059669")])
    s.configure("TEntry", fieldbackground="#1e293b", foreground=fg,
                insertcolor=fg, borderwidth=0)
    s.configure("TCombobox", fieldbackground="#1e293b", foreground=fg,
                background="#1e293b")
    s.configure("Treeview", background="#1e293b", foreground=fg,
                fieldbackground="#1e293b", rowheight=28, borderwidth=0,
                font=("Segoe UI", 10))
    s.configure("Treeview.Heading", background="#334155", foreground="white",
                font=("Segoe UI", 10, "bold"))
    s.map("Treeview", background=[("selected", acc)])

    # Crear cabecera
    h = tk.Frame(root, bg="#1e293b", height=60)
    h.pack(fill="x")
    tk.Label(h, text="🏪  Mi Tienda", bg="#1e293b", fg="white",
              font=("Segoe UI", 18, "bold")).pack(side="left", padx=20, pady=12)
    root.lbl_total = tk.Label(h, text="", bg="#1e293b", fg="#94a3b8",
                              font=("Segoe UI", 10))
    root.lbl_total.pack(side="right", padx=20)
