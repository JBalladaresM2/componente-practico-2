# MÓDULO DE GESTIÓN DE INVENTARIO DE FÁRMACOS
# Este script permite cargar la base de datos de medicamentos desde un archivo de texto,
# procesar la información en estructuras de datos (listas de tuplas) y guardar 
# las actualizaciones de stock y precios de vuelta en el almacenamiento persistente.

def cargar_inventario(ruta):
    # Carga el inventario desde un archivo de texto y lo convierte en lista
    datos_farmacos = []
    try:
        archivo_farmacos = open(ruta, "r")
        for linea in archivo_farmacos:
            # Limpia la línea y separa los datos por comas
            stock, nombre, precio = linea.strip().split(",")
            # Guarda los datos con su tipo de variable correspondiente
            datos_farmacos.append((int(stock), nombre, float(precio)))
        archivo_farmacos.close()
        return datos_farmacos
    except:
        # Manejo de error si el archivo no existe o la ruta es incorrecta
        print("Error... funcion inventario")

def actualizar_inventario(ruta, inventario_cache):
    # Sobrescribe el archivo de texto con los datos actualizados del inventario
    try:
        archivo_farmacos = open(ruta, "w")
        for stock, nombre, precio in inventario_cache:
            # Escribe cada fármaco manteniendo el formato CSV
            archivo_farmacos.write(f"{stock},{nombre},{precio}\n")
        
        print("Inventario actualizado con éxito")
        archivo_farmacos.close()
    except:
        print("Error... funcion actualizar")