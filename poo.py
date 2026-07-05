# clases/medicamento.py
#
# Esta clase representa UN medicamento de la farmacia.
# Piensa en esto como el "molde" con el que se crea cada medicamento.

class Medicamento:

    def __init__(self, nombre, precio, stock, categoria):
        # Este método se llama "constructor". Se ejecuta SOLO cuando
        # se crea un medicamento nuevo, y sirve para guardarle sus datos.
        # "self" significa "este medicamento en específico" (no otro).
        self.nombre = nombre        # Guarda el nombre, ej: "Paracetamol"
        self.precio = precio        # Guarda el precio, ej: 2.50
        self.stock = stock          # Guarda cuántas unidades hay, ej: 100
        self.categoria = categoria  # Guarda el tipo, ej: "Analgésico"

    def aplicar_descuento(self, porcentaje):
        # Este método baja el precio del medicamento según un %.
        # Ejemplo: si le pasas 10, le quita el 10% al precio actual.
        descuento = self.precio * (porcentaje / 100)   # calcula cuánto se descuenta
        self.precio = self.precio - descuento            # actualiza el precio
        print(f"Se aplicó {porcentaje}% de descuento. Nuevo precio: {self.precio}")

    def reducir_stock(self, cantidad):
        # Este método se usa cuando se VENDE el medicamento,
        # para restarle unidades al stock disponible.
        if cantidad > self.stock:
            # Si piden más de lo que hay, no se puede vender.
            print("No hay suficiente stock para esa cantidad.")
        else:
            self.stock = self.stock - cantidad
            print(f"Stock actualizado. Quedan {self.stock} unidades de {self.nombre}.")

    def mostrar_info(self):
        # Este método solo IMPRIME en pantalla los datos del medicamento.
        # No cambia nada, solo muestra.
        print("----------------------------")
        print(f"Nombre: {self.nombre}")
        print(f"Precio: ${self.precio}")
        print(f"Stock: {self.stock}")
        print(f"Categoría: {self.categoria}")
        print("----------------------------")

        # clases/pedido.py
#
# Esta clase representa un PEDIDO, o sea, una compra que hace un cliente.
# Un pedido puede tener VARIOS medicamentos adentro, por eso usamos una lista.

# Traemos la clase Medicamento porque un Pedido va a contener medicamentos.
# (Sin esta línea, Python no sabría qué es "Medicamento" aquí adentro).
from clases.medicamento import Medicamento


class Pedido:

    def __init__(self, cliente):
        # Constructor: se ejecuta cuando se crea un pedido nuevo.
        self.cliente = cliente
        # Esta lista arranca VACÍA. Aquí se van guardando los medicamentos
        # que el cliente va comprando, uno por uno.
        self.medicamentos = []

    def agregar_medicamento(self, medicamento, cantidad):
        # Este método sirve para meter un medicamento dentro del pedido.
        # Recibe dos cosas: el medicamento (un objeto de la clase Medicamento)
        # y la cantidad que el cliente quiere comprar.

        # Primero, le bajamos el stock al medicamento (porque se está vendiendo).
        medicamento.reducir_stock(cantidad)

        # Después, guardamos en la lista un "paquete" con el medicamento
        # y la cantidad, usando un diccionario (como una cajita con etiquetas).
        self.medicamentos.append({
            "medicamento": medicamento,
            "cantidad": cantidad
        })

        print(f"Se agregó {cantidad} unidad(es) de {medicamento.nombre} al pedido de {self.cliente}.")

    def calcular_total(self):
        # Este método recorre TODOS los medicamentos que hay en el pedido
        # y va sumando (precio del medicamento x cantidad comprada).
        total = 0
        for item in self.medicamentos:
            # "item" es cada paquetito (diccionario) que guardamos arriba.
            precio_del_medicamento = item["medicamento"].precio
            cantidad_comprada = item["cantidad"]
            total += precio_del_medicamento * cantidad_comprada
        return total  # Devuelve el número total a pagar.

    def mostrar_resumen(self):
        # Este método imprime en pantalla todo el detalle del pedido,
        # como si fuera el "recibo" o "factura" de la compra.
        print("============================")
        print(f"Resumen del pedido de: {self.cliente}")
        for item in self.medicamentos:
            med = item["medicamento"]
            cant = item["cantidad"]
            print(f"- {med.nombre} x{cant} = ${med.precio * cant}")
        print(f"TOTAL A PAGAR: ${self.calcular_total()}")
        print("============================")
