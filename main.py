# main.py
# ========
# Sistema de Farmacia - Grupo 7
# Encargado principal de este archivo: SEBASTIAN

# Responsabilidades de esta parte:
#  - Menú principal y menús secundarios (interfaz por consola).
#  - Validación de datos ingresados por el usuario (try/except).
#  - Integrar la clase Medicamento y Pedido (Steven) con las funciones
#    de persistencia inventario()/actualizar() (Jonathan).

# NOTA IMPORTANTE:
# La función inventario() de Jonathan devuelve una lista de listas de
# texto (ej: ["Paracetamol", "90", "0.50"]) en el orden nombre, stock,
# precio (así está guardado en datos/medicamentos.txt). La clase
# Medicamento en cambio recibe (nombre, precio, stock). Por eso este
# archivo se encarga de "traducir" entre ambos formatos.

import os
from clases.medicamento import Medicamento
from clases.pedido import Pedido
from modulos.gestion_inventario import inventario, actualizar

# ---------------------------------------------------------------
# PUENTE ENTRE EL FORMATO DE JONATHAN Y LOS OBJETOS DE STEVEN
# ---------------------------------------------------------------

ruta_inventario = "datos/inventario_medicinas.txt"
medicamentos = []

def cargar_medicamentos():
    # Lee el archivo (vía inventario()) y crea objetos Medicamento.
    datos = inventario(ruta_inventario)  # [[nombre, stock, precio], ...]
    if datos is None:
        return []
    
    medicamentos_lista = []
    for stock, nombre, precio in datos:
        # La clase Medicamento recibe (nombre, precio, stock)
        medicamentos_lista.append(Medicamento(stock, nombre, precio))
    return medicamentos_lista

def guardar_medicamentos(medicamentos):
    # Convierte los objetos Medicamento al formato de Jonathan y los guarda.
    cache = [[med.nombre, med.stock, med.precio] for med in medicamentos]
    actualizar(ruta_inventario, cache)

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
        print("⚠ Este campo no puede estar vacío. Intente nuevamente.")

def leer_float(mensaje):
    # Pide un número decimal (precio) y valida el tipo de dato.
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
    # Pide un número entero (stock/cantidad) y valida el tipo de dato.
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
# ---------------------------------------------------------------

def menu_registrar(medicamentos):
    print("\n--- Registrar nuevo medicamento ---")
    nombre = leer_texto("Nombre: ")
    if buscar_por_nombre(medicamentos, nombre):
        print("⚠ Ya existe un medicamento con ese nombre.")
        return
    precio = leer_float("Precio: $")
    stock = leer_entero("Stock inicial: ")

    nuevo = Medicamento(stock, nombre, stock)
    medicamentos.append(nuevo)
    guardar_medicamentos(medicamentos)
    print("✅ Medicamento registrado correctamente.")

def menu_consultar(medicamentos):
    print("\n--- Inventario de medicamentos ---")
    if not medicamentos:
        print("No hay medicamentos registrados.")
        return
    for med in medicamentos:
        med.mostrar_info()

def menu_buscar(medicamentos):
    print("\n--- Buscar medicamento ---")
    texto = leer_texto("Ingrese nombre a buscar: ")
    resultados = buscar_coincidencias(medicamentos, texto)
    if not resultados:
        print("No se encontraron coincidencias.")
    else:
        for med in resultados:
            med.mostrar_info()

def menu_actualizar(medicamentos):
    print("\n--- Actualizar medicamento ---")
    nombre = leer_texto("Nombre del medicamento a actualizar: ")
    med = buscar_por_nombre(medicamentos, nombre)
    if med is None:
        print("⚠ No existe un medicamento con ese nombre.")
        return
    med.mostrar_info()
    print("1. Actualizar precio")
    print("2. Actualizar stock")
    print("3. Aplicar descuento")
    opcion = leer_texto("Seleccione una opción: ")

    if opcion == "1":
        med.precio = leer_float("Nuevo precio: $")
        guardar_medicamentos(medicamentos)
        print("✅ Precio actualizado.")
    elif opcion == "2":
        med.stock = leer_entero("Nuevo stock: ")
        guardar_medicamentos(medicamentos)
        print("✅ Stock actualizado.")
    elif opcion == "3":
        porcentaje = leer_float("Porcentaje de descuento (0-100): ")
        if porcentaje > 100:
            print("⚠ El porcentaje no puede ser mayor a 100.")
        else:
            med.aplicar_descuento(porcentaje)
            guardar_medicamentos(medicamentos)
    else:
        print("⚠ Opción no válida.")

def menu_eliminar(medicamentos):
    print("\n--- Eliminar medicamento ---")
    nombre = leer_texto("Nombre del medicamento a eliminar: ")
    med = buscar_por_nombre(medicamentos, nombre)
    if med is None:
        print("⚠ No existe un medicamento con ese nombre.")
        return
    medicamentos.remove(med)
    guardar_medicamentos(medicamentos)
    print("✅ Medicamento eliminado.")

def menu_crear_pedido(medicamentos):
    print("\n--- Crear nuevo pedido ---")
    cliente = leer_texto("Nombre del cliente: ")
    pedido = Pedido(cliente)

    while True:
        nombre_med = leer_texto("Nombre del medicamento a agregar: ")
        med = buscar_por_nombre(medicamentos, nombre_med)
        if med is None:
            print("⚠ No existe un medicamento con ese nombre.")
        else:
            med.mostrar_info()
            cantidad = leer_entero("Cantidad: ")
            if cantidad > med.stock:
                print("⚠ No hay suficiente stock para esa cantidad.")
            else:
                pedido.agregar_medicamento(med, cantidad)

        otro = leer_texto("¿Agregar otro medicamento? (s/n): ").lower()
        if otro != "s":
            break

    if not pedido.medicamentos:
        print("⚠ El pedido quedó vacío, no se guardará.")
        return

    pedido.mostrar_resumen()
    guardar_medicamentos(medicamentos)  # persiste el stock ya descontado
    print("✅ Pedido registrado. Stock actualizado en datos/inventario.txt")

def menu_inspeccionar_archivo():
    # Demostración de manejo de streams:
    # abre el archivo de medicamentos, muestra sus atributos (name, mode,
    # closed), lee una porción con read(), reporta la posición del cursor
    # con tell(), y usa seek() para regresar al inicio antes de leer
    # línea por línea con readline().
    print("\n--- Inspección del stream (datos/inventario_medicinas.txt) ---")
    ruta = os.path.join("datos", "inventario_medicinas.txt")

    if not os.path.exists(ruta):
        print("⚠ Todavía no existe el archivo. Registra al menos un medicamento primero.")
        return

    archivo = open(ruta, "r", encoding="utf-8")  # abrimos el stream manualmente

    print(f"Nombre del archivo (archivo.name): {archivo.name}")
    print(f"Modo de apertura (archivo.mode): {archivo.mode}")
    print(f"¿Está cerrado? (archivo.closed): {archivo.closed}")

    fragmento = archivo.read(25)
    print(f"\nPrimeros 25 caracteres (read(25)): {fragmento!r}")

    posicion = archivo.tell()
    print(f"Posición actual del cursor (tell()): {posicion}")

    archivo.seek(0)  # rebobinamos el stream al inicio
    print("Cursor regresado al inicio con seek(0).")

    primera_linea = archivo.readline()
    print(f"Primera línea del archivo (readline()): {primera_linea.strip()}")

    archivo.close()  # liberamos el recurso para evitar fugas de memoria
    print(f"Archivo cerrado correctamente (archivo.closed): {archivo.closed}")

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
    print("6. Crear pedido (venta)")
    print("7. Inspeccionar archivo (streams: read, tell, seek)")
    print("8. Salir")

def main():
    medicamentos = cargar_medicamentos()  # persistencia: se cargan loa datos guardados

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
            menu_crear_pedido(medicamentos)
        elif opcion == "7":
            menu_inspeccionar_archivo()
        elif opcion == "8":
            print("Gracias por usar el sistema. ¡Hasta luego!")
            break
        else:
            print("⚠ Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()