"""Módulo de definición de la clase Pedido.

Representa una transacción de venta o pedido de un cliente en la farmacia,
agrupando múltiples medicamentos y generando los registros para el historial.
"""

from clases.medicamento import Medicamento


class Pedido:
    """Modelo que representa un pedido de compra realizado por un cliente."""

    def __init__(self, cliente):
        """Inicializa un nuevo pedido con el nombre del cliente y una lista vacía de ítems."""
        self.cliente = str(cliente)
        self.medicamentos = []

    def agregar_medicamento(self, medicamento, cantidad):
        """Agrega un medicamento al pedido y reduce su stock en el inventario."""
        medicamento.reducir_stock(cantidad)
        self.medicamentos.append({
            "medicamento": medicamento,
            "cantidad": int(cantidad)
        })
        print(f"Se agregó {cantidad} unidad(es) de {medicamento.nombre} al pedido de {self.cliente}.")

    def calcular_total(self):
        """Calcula el costo total sumando el precio por cantidad de cada ítem."""
        total = 0.0
        for item in self.medicamentos:
            precio = item["medicamento"].precio
            cantidad = item["cantidad"]
            total += precio * cantidad
        return total

    def mostrar_resumen(self):
        """Muestra por consola el detalle y el total a pagar del pedido."""
        print("============================")
        print(f"Resumen del pedido de: {self.cliente}")
        for item in self.medicamentos:
            med = item["medicamento"]
            cant = item["cantidad"]
            subtotal = med.precio * cant
            print(f"- {med.nombre} x{cant} = ${subtotal:.2f}")
        print(f"TOTAL A PAGAR: ${self.calcular_total():.2f}")
        print("============================")

    def a_filas_registro(self):
        """Genera una lista de filas [cliente, cantidad, nombre, precio] para el registro de ventas."""
        filas = []
        for item in self.medicamentos:
            med = item["medicamento"]
            cant = item["cantidad"]
            filas.append([self.cliente, cant, med.nombre, med.precio])
        return filas

