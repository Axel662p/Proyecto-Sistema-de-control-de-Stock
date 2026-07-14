import sqlite3
import threading

DB = "tienda.db"

class database:
    """Gestor de conexión a base de datos con thread-safety"""
    
    @staticmethod
    def conectar():
        """Crear conexión y tablas si no existen"""
        con = sqlite3.connect(DB, check_same_thread=False)

        con.execute("""
        CREATE TABLE IF NOT EXISTS productos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            categoria TEXT,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )""")

        con.execute("""
        CREATE TABLE IF NOT EXISTS ventas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY(producto_id) REFERENCES productos(id)
        )""")

        con.commit()
        return con
