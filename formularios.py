"""Utilidades para formularios"""

class FormularioValidator:
    """Validador de formularios"""
    
    @staticmethod
    def validar_numero(valor):
        """Validar que sea un número"""
        try:
            return float(valor), True
        except ValueError:
            return None, False

    @staticmethod
    def validar_entero(valor):
        """Validar que sea un entero"""
        try:
            return int(valor), True
        except ValueError:
            return None, False

    @staticmethod
    def validar_positivo(valor):
        """Validar que sea positivo"""
        try:
            v = float(valor)
            return v, v >= 0
        except ValueError:
            return None, False

    @staticmethod
    def limpiar_entrada(texto):
        """Limpiar entrada de texto"""
        return texto.strip()
