# MÓDULO DE GESTIÓN DE INVENTARIO DE FÁRMACOS
# Este script permite cargar la base de datos de medicamentos desde un archivo de texto,
# procesar la información en estructuras de datos (listas de tuplas) y guardar 
# las actualizaciones de stock y precios de vuelta en el almacenamiento persistente.

def cargar_archivo(ruta):
    # Carga el inventario desde un archivo de texto y lo convierte en lista
    datos_archivo = []
    try:
        archivo = open(ruta, "r")
        for linea in archivo:
            # Limpia la línea y separa los datos por comas
            entero, texto, decimal = linea.strip().split(",")
            # Guarda los datos con su tipo de variable correspondiente
            datos_archivo.append((int(entero), texto, float(decimal)))
        archivo.close()
        return datos_archivo
    except:
        # Manejo de error si el archivo no existe o la ruta es incorrecta
        print(f"Error... funcion cargar archivo - {ruta}")

def actualizar_archivo(ruta, datos_cache):
    # Sobrescribe el archivo de texto con los datos actualizados del inventario
    try:
        archivo = open(ruta, "w")
        for entero, texto, decimal in datos_cache:
            # Escribe cada fármaco manteniendo el formato CSV
            archivo.write(f"{entero},{texto},{decimal}\n")
        archivo.close()
    except:
        print(f"Error... funcion actualizar archivo - {ruta}")