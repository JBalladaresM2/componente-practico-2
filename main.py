"""
main.py
========
Sistema de Farmacia - Grupo 7
Encargado principal de este archivo: SEBASTIAN

Responsabilidades de esta parte:
 - Menú principal y menús secundarios (interfaz por consola).
 - Validación de datos ingresados por el usuario (try/except).
 - Integrar las clases de Steven (clases/) y las funciones de
   Jonathan (modulos/) para que el sistema funcione sin errores.
"""

from clases.medicamento import Medicamento
from clases.venta import Venta
from modulos import gestion_medicamentos as gm
from modulos import gestion_ventas as gv


# ---------------------------------------------------------------
# FUNCIONES DE VALIDACIÓN
# Evitan que el programa se caiga si el usuario ingresa texto
# donde se esperaba un número.
# ---------------------------------------------------------------

def leer_texto(mensaje):
    """Pide un texto y valida que no esté vacío."""
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("⚠ Este campo no puede estar vacío. Intente nuevamente.")


def leer_float(mensaje):
    """Pide un número decimal (precio) y valida el tipo de dato."""
    while True:
        valor = input(mensaje).strip()
        try:
            numero = float(valor)
            if numero < 0:
                print("⚠ El valor no puede ser negativo.")
                continue
            return numero
        except ValueError:
            print("⚠ Debe ingresar un número válido (ej: 12.50).")


def leer_entero(mensaje):
    """Pide un número entero (stock/cantidad) y valida el tipo de dato."""
    while True:
        valor = input(mensaje).strip()
        try:
            numero = int(valor)
            if numero < 0:
                print("⚠ El valor no puede ser negativo.")
                continue
            return numero
        except ValueError:
            print("⚠ Debe ingresar un número entero válido (ej: 10).")


# ---------------------------------------------------------------
# MENÚS SECUNDARIOS
# Cada función corresponde a una opción del menú principal.
# ---------------------------------------------------------------

def menu_registrar(medicamentos):
    print("\n--- Registrar nuevo medicamento ---")
    codigo = leer_texto("Código: ")
    if gm.buscar_por_codigo(medicamentos, codigo):
        print("⚠ Ya existe un medicamento con ese código.")
        return
    nombre = leer_texto("Nombre: ")
    categoria = leer_texto("Categoría: ")
    precio = leer_float("Precio: $")
    stock = leer_entero("Stock inicial: ")
    laboratorio = leer_texto("Laboratorio: ")

    nuevo = Medicamento(codigo, nombre, categoria, precio, stock, laboratorio)
    gm.registrar_medicamento(medicamentos, nuevo)
    print("✅ Medicamento registrado correctamente.")


def menu_consultar(medicamentos):
    print("\n--- Inventario de medicamentos ---")
    if not medicamentos:
        print("No hay medicamentos registrados.")
        return
    for med in medicamentos:
        print(med)


def menu_buscar(medicamentos):
    print("\n--- Buscar medicamento ---")
    texto = leer_texto("Ingrese nombre o categoría a buscar: ")
    resultados = gm.buscar_por_nombre_o_categoria(medicamentos, texto)
    if not resultados:
        print("No se encontraron coincidencias.")
    else:
        for med in resultados:
            print(med)


def menu_actualizar(medicamentos):
    print("\n--- Actualizar medicamento ---")
    codigo = leer_texto("Código del medicamento a actualizar: ")
    med = gm.buscar_por_codigo(medicamentos, codigo)
    if med is None:
        print("⚠ No existe un medicamento con ese código.")
        return
    print(med)
    print("1. Actualizar precio")
    print("2. Actualizar stock")
    print("3. Aplicar descuento")
    opcion = leer_texto("Seleccione una opción: ")

    if opcion == "1":
        nuevo_precio = leer_float("Nuevo precio: $")
        gm.actualizar_medicamento(medicamentos, codigo, nuevo_precio=nuevo_precio)
        print("✅ Precio actualizado.")
    elif opcion == "2":
        nuevo_stock = leer_entero("Nuevo stock: ")
        gm.actualizar_medicamento(medicamentos, codigo, nuevo_stock=nuevo_stock)
        print("✅ Stock actualizado.")
    elif opcion == "3":
        porcentaje = leer_float("Porcentaje de descuento (0-100): ")
        try:
            med.aplicar_descuento(porcentaje)
            gm.guardar_medicamentos(medicamentos)
            print(f"✅ Descuento aplicado. Nuevo precio: ${med.precio:.2f}")
        except ValueError as error:
            print(f"⚠ {error}")
    else:
        print("⚠ Opción no válida.")


def menu_eliminar(medicamentos):
    print("\n--- Eliminar medicamento ---")
    codigo = leer_texto("Código del medicamento a eliminar: ")
    if gm.eliminar_medicamento(medicamentos, codigo):
        print("✅ Medicamento eliminado.")
    else:
        print("⚠ No existe un medicamento con ese código.")


def menu_vender(medicamentos):
    print("\n--- Registrar venta ---")
    codigo = leer_texto("Código del medicamento: ")
    med = gm.buscar_por_codigo(medicamentos, codigo)
    if med is None:
        print("⚠ No existe un medicamento con ese código.")
        return
    print(med)
    cantidad = leer_entero("Cantidad a vender: ")
    try:
        med.actualizar_stock(-cantidad)  # resta stock, valida que no sea negativo
    except ValueError as error:
        print(f"⚠ {error}")
        return
    gm.guardar_medicamentos(medicamentos)
    venta = Venta(med, cantidad)
    gv.registrar_venta(venta)
    print(f"✅ Venta registrada: {venta}")


# ---------------------------------------------------------------
# MENÚ PRINCIPAL Y FLUJO GENERAL DEL PROGRAMA
# ---------------------------------------------------------------

def mostrar_menu():
    print("\n===== SISTEMA DE FARMACIA - GRUPO 7 =====")
    print("1. Registrar medicamento")
    print("2. Consultar inventario")
    print("3. Buscar medicamento")
    print("4. Actualizar medicamento")
    print("5. Eliminar medicamento")
    print("6. Registrar venta")
    print("7. Salir")


def main():
    medicamentos = gm.cargar_medicamentos()  # persistencia: se carga lo guardado antes

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            menu_registrar(medicamentos)
        elif opcion == "2":
            menu_consultar(medicamentos)
        elif opcion == "3":
            menu_buscar(medicamentos)
        elif opcion == "4":
            menu_actualizar(medicamentos)
        elif opcion == "5":
            menu_eliminar(medicamentos)
        elif opcion == "6":
            menu_vender(medicamentos)
        elif opcion == "7":
            print("Gracias por usar el sistema. ¡Hasta luego!")
            break
        else:
            print("⚠ Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()
