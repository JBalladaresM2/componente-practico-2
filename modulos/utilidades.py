"""Módulo de utilidades generales del sistema de farmacia.

Contiene funciones de validación de entradas por teclado para prevenir fallos
de ejecución y herramientas de búsqueda dentro del inventario.
"""


def leer_texto(mensaje):
    """Solicita una cadena de texto por consola y valida que no esté vacía."""
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("Este campo no puede estar vacío. Intente nuevamente.")


def leer_float(mensaje):
    """Solicita un número decimal positivo por consola y valida el tipo de dato."""
    while True:
        valor = input(mensaje).strip()
        try:
            numero = float(valor)
            if numero < 0:
                print("El valor no puede ser negativo.")
                continue
            return numero
        except ValueError:
            print("Debe ingresar un número válido (ej: 12.50).")


def leer_entero(mensaje):
    """Solicita un número entero positivo por consola y valida el tipo de dato."""
    while True:
        valor = input(mensaje).strip()
        try:
            numero = int(valor)
            if numero < 0:
                print("El valor no puede ser negativo.")
                continue
            return numero
        except ValueError:
            print("Debe ingresar un número entero válido (ej: 10).")


def buscar_por_nombre(medicamentos, nombre):
    """Busca y retorna un medicamento por su nombre exacto (sin distinguir mayúsculas)."""
    for med in medicamentos:
        if med.nombre.lower() == nombre.lower():
            return med
    return None


def buscar_coincidencias(medicamentos, texto):
    """Retorna una lista de medicamentos cuyo nombre contenga el texto buscado."""
    texto = texto.lower()
    return [med for med in medicamentos if texto in med.nombre.lower()]
