# clases/pedido.py
#
# Esta clase representa un PEDIDO, o sea, una compra de un cliente.
# Un pedido puede tener VARIOS medicamentos adentro, por eso usamos una lista.

# Traemos la clase Medicamento porque un Pedido va a contener medicamentos.
from clases.medicamento import Medicamento


class Pedido:

    def __init__(self, cliente):
        # Constructor: se ejecuta cuando se crea un pedido nuevo.
        self.cliente = cliente
        # Lista vacía donde se van guardando los medicamentos comprados.
        self.medicamentos = []

    def agregar_medicamento(self, medicamento, cantidad):
        # Mete un medicamento dentro del pedido.
        # Recibe el medicamento (objeto de la clase Medicamento) y la cantidad.

        # Primero bajamos el stock, porque se está vendiendo.
        medicamento.reducir_stock(cantidad)

        # Guardamos el medicamento y su cantidad en la lista,
        # usando un diccionario (una cajita con dos etiquetas).
        self.medicamentos.append({
            "medicamento": medicamento,
            "cantidad": cantidad
        })

        print(f"Se agregó {cantidad} unidad(es) de {medicamento.nombre} al pedido de {self.cliente}.")

    def calcular_total(self):
        # Recorre todos los medicamentos del pedido
        # y va sumando (precio x cantidad) de cada uno.
        total = 0
        for item in self.medicamentos:
            precio_del_medicamento = item["medicamento"].precio
            cantidad_comprada = item["cantidad"]
            total += precio_del_medicamento * cantidad_comprada
        return total

    def mostrar_resumen(self):
        # Imprime el "recibo" completo del pedido.
        print("============================")
        print(f"Resumen del pedido de: {self.cliente}")
        for item in self.medicamentos:
            med = item["medicamento"]
            cant = item["cantidad"]
            print(f"- {med.nombre} x{cant} = ${med.precio * cant}")
        print(f"TOTAL A PAGAR: ${self.calcular_total()}")
        print("============================")