# clases/medicamento.py
#
# Esta clase representa UN medicamento de la farmacia.
# Es como el "molde" con el que se crea cada medicamento nuevo.

class Medicamento:

    def __init__(self, nombre, precio, stock, categoria):
        # Este método es el "constructor". Se ejecuta SOLO
        # cuando se crea un medicamento nuevo, y guarda sus datos.
        # "self" significa "este medicamento en específico" (no otro).
        self.nombre = nombre        # Guarda el nombre, ej: "Paracetamol"
        self.precio = precio        # Guarda el precio, ej: 2.50
        self.stock = stock          # Guarda cuántas unidades hay, ej: 100
        self.categoria = categoria  # Guarda el tipo, ej: "Analgésico"

    def aplicar_descuento(self, porcentaje):
        # Baja el precio según un porcentaje.
        # Ejemplo: si le pasas 10, le quita el 10% al precio actual.
        descuento = self.precio * (porcentaje / 100)
        self.precio = self.precio - descuento
        print(f"Se aplicó {porcentaje}% de descuento. Nuevo precio: {self.precio}")

    def reducir_stock(self, cantidad):
        # Se usa cuando se VENDE el medicamento, para bajar el stock.
        if cantidad > self.stock:
            print("No hay suficiente stock para esa cantidad.")
        else:
            self.stock = self.stock - cantidad
            print(f"Stock actualizado. Quedan {self.stock} unidades de {self.nombre}.")

    def mostrar_info(self):
        # Solo IMPRIME los datos del medicamento, no cambia nada.
        print("----------------------------")
        print(f"Nombre: {self.nombre}")
        print(f"Precio: ${self.precio}")
        print(f"Stock: {self.stock}")
        print(f"Categoría: {self.categoria}")
        print("----------------------------")