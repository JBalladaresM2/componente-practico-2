# MÓDULO DE GESTIÓN DE INVENTARIO DE FÁRMACOS
# Este script permite cargar la base de datos de medicamentos desde un archivo de texto,
# procesar la información en estructuras de datos (listas de tuplas) y guardar 
# las actualizaciones de stock y precios de vuelta en el almacenamiento persistente.

def evaluar_y_convertir(valor):
    # Detecta de forma independiente si un texto es entero, decimal o string.
    valor = valor.strip() # Remueve espacios en blanco innecesarios en los extremos
    
    # Intenta la conversión a entero (ej: "5" -> 5)
    try:
        return int(valor)
    except ValueError:
        pass # Si falla (ej: tiene letras o puntos), ignora el error y continúa
        
    # Intenta la conversión a decimal/punto flotante (ej: "0.3" -> 0.3)
    try:
        return float(valor)
    except ValueError:
        pass # Si también falla (ej: es puro texto), ignora el error
        
    # Si no se pudo convertir a ningún número, se retorna el valor original como string
    return valor


def cargar_archivo(ruta):
    # Carga el inventario desde un archivo de texto y lo convierte en lista
    datos_archivo_procesados = []

    try:
        archivo = open(ruta, "r") # Abre el archivo en modo lectura
        for linea in archivo:
            # 1. Limpiamos espacios y saltos de línea, y fragmentamos la cadena por cada coma
            datos_archivo = linea.strip().split(",")
            
            # 2. CONVERSIÓN AUTOMÁTICA: Recorre cada fragmento de la línea de forma dinámica,
            # evaluando individualmente si corresponde a int, float o string.
            linea_procesada = [evaluar_y_convertir(dato) for dato in datos_archivo]
            
            # 3. Guardamos la línea ya convertida (como una sublista de datos tipados) en nuestra lista principal
            datos_archivo_procesados.append(linea_procesada)
            
        archivo.close() # Cierra el flujo del archivo para liberar memoria en el sistema
        return datos_archivo_procesados # Retorna la matriz/lista de listas con el inventario
    except Exception as e:
        # Atrapa cualquier fallo (ej: archivo inexistente o problemas de permisos) y muestra el detalle
        print(f"Error inesperado en cargar archivo - {ruta}: {e}")

def actualizar_archivo(ruta, datos_cache):
    # Sobrescribe el archivo de texto con los datos actualizados del inventario
    try:
        archivo = open(ruta, "w") # Abre el archivo en modo escritura (borra el contenido previo)
        linea = "" # Variable acumuladora para construir todo el bloque de texto a escribir
        
        for cache in datos_cache:
            # Escribe cada fármaco manteniendo el formato CSV
            for dato in cache:
                linea += f"{dato}," # Concatena cada dato seguido de una coma
                
            # Remueve la última coma sobrante de la fila [:-1] y añade un salto de línea [+\n]
            linea = linea[:-1] + "\n"
            
        archivo.write(linea) # Guarda físicamente todo el string estructurado en el archivo de texto
        archivo.close() # Cierra el archivo de forma segura
    except Exception as e:
        # Captura errores en caso de que el archivo esté protegido o la ruta no sea válida
        print(f"Error inesperado en actualizar archivo - {ruta}: {e}")