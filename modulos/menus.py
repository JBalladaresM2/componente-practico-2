"""Módulo de menús e interfaz de usuario por consola.

Contiene las funciones visuales y de interacción con el usuario para gestionar
el inventario de medicamentos y el registro de pedidos, comunicándose
directamente con los archivos de persistencia sin intermediarios.
"""

import os
from clases.medicamento import Medicamento
from clases.pedido import Pedido
from modulos.gestion_archivos import actualizar_archivo
from modulos.utilidades import (
    leer_texto,
    leer_float,
    leer_entero,
    buscar_por_nombre,
    buscar_coincidencias,
)

RUTA_INV_MED = "datos/inventario_medicinas.txt"
RUTA_REG_PED = "datos/registro_pedidos.txt"


def mostrar_menu_principal():
    """Muestra por consola las opciones principales del sistema."""
    print("===== SISTEMA DE FARMACIA - GRUPO 7 =====")
    print("1. Registrar medicamento")  # GESTIONAR MEDICAMENTOS
    print("2. Actualizar medicamento") # GESTIONAR MEDICAMENTOS
    print("3. Buscar medicamento")     # GESTIONAR INVENTARIO
    print("4. Consultar inventario")   # GESTIONAR INVENTARIO
    print("5. Eliminar medicamento")   # GESTIONAR INVENTARIO
    print("6. Crear pedido (venta)")   # GESTIONAR VENTAS
    print("7. Consultar pedidos")      # GESTIONAR VENTAS
    print("8. Salir")


def menu_registrar(medicamentos):
    """Permite registrar un nuevo medicamento y lo guarda directamente en el archivo."""
    print("--- Registrar nuevo medicamento ---")
    nombre = leer_texto("Nombre: ")
    if buscar_por_nombre(medicamentos, nombre):
        print("Ya existe un medicamento con ese nombre.")
        input()
        os.system("cls")
        return
    precio = leer_float("Precio: $")
    stock = leer_entero("Stock inicial: ")

    nuevo = Medicamento(stock, nombre, precio)
    medicamentos.append(nuevo)
    
    # Comunicación directa con persistencia: cada objeto se convierte a lista
    actualizar_archivo(RUTA_INV_MED, [med.a_lista() for med in medicamentos])
    print("Medicamento registrado correctamente.")
    input()
    os.system("cls")


def menu_consultar(medicamentos):
    """Muestra el listado completo de medicamentos en el inventario."""
    print("--- Inventario de medicamentos ---")
    if not medicamentos:
        print("No hay medicamentos registrados.")
        input()
        os.system("cls")
        return
    for med in medicamentos:
        med.mostrar_info()
    input()
    os.system("cls")


def menu_buscar(medicamentos):
    """Permite buscar medicamentos por coincidencia parcial de nombre."""
    print("--- Buscar medicamento ---")
    texto = leer_texto("Ingrese nombre a buscar: ")
    resultados = buscar_coincidencias(medicamentos, texto)
    if not resultados:
        print("No se encontraron coincidencias.")
    else:
        for med in resultados:
            med.mostrar_info()
    input()
    os.system("cls")


def menu_actualizar(medicamentos):
    """Permite modificar el precio, stock o aplicar descuentos a un medicamento."""
    print("--- Actualizar medicamento ---")
    nombre = leer_texto("Nombre del medicamento a actualizar: ")
    med = buscar_por_nombre(medicamentos, nombre)
    if med is None:
        print("No existe un medicamento con ese nombre.")
        input()
        os.system("cls")
        return
    med.mostrar_info()
    print("1. Actualizar precio")
    print("2. Actualizar stock")
    print("3. Aplicar descuento")
    opcion = leer_texto("Seleccione una opción: ")

    if opcion == "1":
        med.precio = leer_float("Nuevo precio: $")
        actualizar_archivo(RUTA_INV_MED, [m.a_lista() for m in medicamentos])
        print("Precio actualizado.")
    elif opcion == "2":
        med.stock = leer_entero("Nuevo stock: ")
        actualizar_archivo(RUTA_INV_MED, [m.a_lista() for m in medicamentos])
        print("Stock actualizado.")
    elif opcion == "3":
        porcentaje = leer_float("Porcentaje de descuento (0-100): ")
        if porcentaje > 100:
            print("El porcentaje no puede ser mayor a 100.")
        else:
            med.aplicar_descuento(porcentaje)
            actualizar_archivo(RUTA_INV_MED, [m.a_lista() for m in medicamentos])
    else:
        print("Opción no válida.")
        
    input()
    os.system("cls")


def menu_eliminar(medicamentos):
    """Permite eliminar un medicamento del inventario y actualiza el archivo directamente."""
    print("--- Eliminar medicamento ---")
    nombre = leer_texto("Nombre del medicamento a eliminar: ")
    med = buscar_por_nombre(medicamentos, nombre)
    if med is None:
        print("No existe un medicamento con ese nombre.")
        input()
        os.system("cls")
        return
    medicamentos.remove(med)
    actualizar_archivo(RUTA_INV_MED, [m.a_lista() for m in medicamentos])
    print("Medicamento eliminado.")
    input()
    os.system("cls")


def menu_crear_pedido(medicamentos, historial_pedidos):
    """Crea una orden de compra con múltiples ítems, reduciendo stock y guardando el registro."""
    print("--- Crear nuevo pedido ---")
    cliente = leer_texto("Nombre del cliente: ")
    pedido = Pedido(cliente)

    while True:
        nombre_med = leer_texto("Nombre del medicamento a agregar: ")
        med = buscar_por_nombre(medicamentos, nombre_med)
        if med is None:
            print("No existe un medicamento con ese nombre.")
            input()
            os.system("cls")
        else:
            med.mostrar_info()
            cantidad = leer_entero("Cantidad: ")
            if cantidad > med.stock:
                print("No hay suficiente stock para esa cantidad.")
                input()
                os.system("cls")
            else:
                pedido.agregar_medicamento(med, cantidad)

        otro = leer_texto("¿Agregar otro medicamento? (s/n): ").lower()
        if otro != "s":
            os.system("cls")
            break
        os.system("cls")

    if not pedido.medicamentos:
        print("El pedido quedó vacío, no se guardará.")
        input()
        os.system("cls")
        return

    pedido.mostrar_resumen()
    
    # Comunicación directa: el pedido genera sus filas para el registro
    historial_pedidos.extend(pedido.a_filas_registro())
    
    # Persistencia directa de inventario y pedidos
    actualizar_archivo(RUTA_INV_MED, [med.a_lista() for med in medicamentos])
    actualizar_archivo(RUTA_REG_PED, historial_pedidos)
    print("Pedido registrado correctamente.")
    input()
    os.system("cls")


def menu_consultar_pedidos(historial_pedidos):
    """Muestra el historial completo de ventas registradas."""
    print("--- Registros de Pedidos ---")
    if not historial_pedidos:
        print("No hay pedidos registrados.")
        input()
        os.system("cls")
        return
    for venta in historial_pedidos:
        print("----------------------------")
        print(f"Cliente: {venta[0]}")
        print(f"Cantidad: {venta[1]}")
        print(f"Nombre: {venta[2]}")
        print(f"Precio: ${float(venta[3]):.2f}")
        print("----------------------------")
    input()
    os.system("cls")
