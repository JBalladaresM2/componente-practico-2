"""Módulo de definición de la clase Medicamento.

Representa un fármaco dentro del inventario de la farmacia y gestiona
su stock, precio y serialización de datos.
"""


class Medicamento:
    """Modelo que representa un medicamento en el inventario."""

    def __init__(self, stock, nombre, precio):
        """Inicializa un medicamento con stock, nombre y precio unitario."""
        self.stock = int(stock)
        self.nombre = str(nombre)
        self.precio = float(precio)

    def aplicar_descuento(self, porcentaje):
        """Aplica un porcentaje de descuento (0 a 100) sobre el precio actual."""
        descuento = self.precio * (porcentaje / 100)
        self.precio -= descuento
        print(f"Se aplicó {porcentaje}% de descuento. Nuevo precio: ${self.precio:.2f}")

    def reducir_stock(self, cantidad):
        """Disminuye el stock disponible al realizar una venta."""
        if cantidad > self.stock:
            print("No hay suficiente stock para esa cantidad.")
        else:
            self.stock -= cantidad
            print(f"Stock actualizado. Quedan {self.stock} unidades de {self.nombre}.")

    def mostrar_info(self):
        """Muestra por consola la información general del medicamento."""
        print("----------------------------")
        print(f"Nombre: {self.nombre}")
        print(f"Precio: ${self.precio:.2f}")
        print(f"Stock: {self.stock}")
        print("----------------------------")

    def a_lista(self):
        """Convierte el objeto en una lista estándar [stock, nombre, precio] para guardado."""
        return [self.stock, self.nombre, self.precio]

    @classmethod
    def desde_lista(cls, datos):
        """Crea una instancia de Medicamento a partir de una lista [stock, nombre, precio]."""
        stock, nombre, precio = datos[0], datos[1], datos[2]
        return cls(stock, nombre, precio)

