# ARCHIVO PRINCIPAL
# ========
# Sistema de Farmacia - Grupo 7
# Encargado principal de este archivo: SEBASTIAN

# Responsabilidades de esta parte:
#  - Menú principal y menús secundarios (interfaz por consola).
#  - Validación de datos ingresados por el usuario (try/except).
#  - Integrar la clase Medicamento y Pedido (Steven) con las funciones
#    de persistencia cargar_inventario()/actualizar_inventario() (Jonathan).

import os
from clases.medicamento import Medicamento
from clases.pedido import Pedido
from modulos.gestion_inventario import cargar_inventario, actualizar_inventario

# ---------------------------------------------------------------
# PUENTE ENTRE EL FORMATO DE JONATHAN Y LOS OBJETOS DE STEVEN
# ---------------------------------------------------------------

ruta_inventario = "datos/inventario_medicinas.txt"

def cargar_medicamentos():
    # Lee el archivo (vía inventario()) y crea objetos Medicamento.
    datos = cargar_inventario(ruta_inventario)
    if datos is None:
        return []

    medicamentos_lista = []
    for stock, nombre, precio in datos:
        # La clase Medicamento recibe (nombre, precio, stock)
        medicamentos_lista.append(Medicamento(stock, nombre, precio))
    return medicamentos_lista

def guardar_medicamentos(medicamentos):
    # Convierte los objetos Medicamento al formato de Jonathan y los guarda.
    cache = [[med.stock, med.nombre, med.precio] for med in medicamentos]
    actualizar_inventario(ruta_inventario, cache)

def buscar_por_nombre(medicamentos, nombre):
    # Búsqueda exacta por nombre (no hay código único en esta versión).
    for med in medicamentos:
        if med.nombre.lower() == nombre.lower():
            return med
    return None

def buscar_coincidencias(medicamentos, texto):
    # Búsqueda parcial por nombre.
    texto = texto.lower()
    return [m for m in medicamentos if texto in m.nombre.lower()]

# ---------------------------------------------------------------
# FUNCIONES DE VALIDACIÓN
# Evitan que el programa se caiga si el usuario ingresa texto
# donde se esperaba un número.
# ---------------------------------------------------------------

def leer_texto(mensaje):
    # Pide un texto y valida que no esté vacío.
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("Este campo no puede estar vacío. Intente nuevamente.")

def leer_float(mensaje):
    # Pide un número decimal (precio) y valida el tipo de dato.
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
    # Pide un número entero (stock/cantidad) y valida el tipo de dato.
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

# ---------------------------------------------------------------
# MENÚS SECUNDARIOS
# ---------------------------------------------------------------

def menu_registrar(medicamentos):
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
    guardar_medicamentos(medicamentos)
    print("Medicamento registrado correctamente.")
    input()
    os.system("cls")

def menu_consultar(medicamentos):
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
    print("--- Buscar medicamento ---")
    texto = leer_texto("Ingrese nombre a buscar: ")
    resultados = buscar_coincidencias(medicamentos, texto)
    if not resultados:
        print("No se encontraron coincidencias.")
        input()
        os.system("cls")
    else:
        for med in resultados:
            med.mostrar_info()
        input()
        os.system("cls")

def menu_actualizar(medicamentos):
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
        guardar_medicamentos(medicamentos)
        print("Precio actualizado.")
        input()
        os.system("cls")
    elif opcion == "2":
        med.stock = leer_entero("Nuevo stock: ")
        guardar_medicamentos(medicamentos)
        print("Stock actualizado.")
        input()
        os.system("cls")
    elif opcion == "3":
        porcentaje = leer_float("Porcentaje de descuento (0-100): ")
        if porcentaje > 100:
            print("El porcentaje no puede ser mayor a 100.")
            input()
            os.system("cls")
        else:
            med.aplicar_descuento(porcentaje)
            guardar_medicamentos(medicamentos)
            input()
            os.system("cls")
    else:
        print("Opción no válida.")
        input()
        os.system("cls")

def menu_eliminar(medicamentos):
    print("--- Eliminar medicamento ---")
    nombre = leer_texto("Nombre del medicamento a eliminar: ")
    med = buscar_por_nombre(medicamentos, nombre)
    if med is None:
        print("No existe un medicamento con ese nombre.")
        input()
        os.system("cls")
        return
    medicamentos.remove(med)
    guardar_medicamentos(medicamentos)
    print("Medicamento eliminado.")
    input()
    os.system("cls")

def menu_crear_pedido(medicamentos):
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
        print("pedido quedó vacío, no se guardará.")
        input()
        os.system("cls")
        return

    pedido.mostrar_resumen()
    guardar_medicamentos(medicamentos)  # persiste el stock ya descontado
    print("Pedido registrado.")
    input()
    os.system("cls")

# ---------------------------------------------------------------
# MENÚ PRINCIPAL Y FLUJO GENERAL DEL PROGRAMA
# ---------------------------------------------------------------

os.system("cls")

def mostrar_menu():
    print("===== SISTEMA DE FARMACIA - GRUPO 7 =====")
    print("1. Registrar medicamento")  # GESTIONAR MEDICAMENTOS
    print("2. Actualizar medicamento") # GESTIONAR MEDICAMENTOS
    print("3. Buscar medicamento")     # GESTIONAR INVENTARIO
    print("4. Consultar inventario")   # GESTIONAR INVENTARIO
    print("5. Eliminar medicamento")   # GESTIONAR INVENTARIO
    print("6. Crear pedido (venta)")   # GESTIONAR VENTAS
    print("7. Consultar pedidos")      # GESTIONAR VENTAS
    print("8. Salir")
# APLICACION
medicamentos = cargar_medicamentos()  # persistencia: se cargan loa datos guardados

while True:
    mostrar_menu()
    opcion = input("Seleccione una opción: ").strip()
    os.system("cls")
    
    if opcion == "1":
        menu_registrar(medicamentos)
    elif opcion == "2":
        menu_actualizar(medicamentos)
    elif opcion == "3":
        menu_buscar(medicamentos)
    elif opcion == "4":
        menu_consultar(medicamentos)
    elif opcion == "5":
        menu_eliminar(medicamentos)
    elif opcion == "6":
        menu_crear_pedido(medicamentos)
    elif opcion == "6":
        continue
    elif opcion == "8":
        print("¡Hasta luego!")
        break
    else:
        print("Opción no válida, intente nuevamente.")