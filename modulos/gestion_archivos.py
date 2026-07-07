"""Módulo de gestión de archivos de texto y CSV.

Proporciona funciones de bajo nivel para leer y escribir datos tabulares
en archivos de texto, utilizando manejo de contextos seguro (with open)
y conversión automática de tipos (int, float, str).
"""


def evaluar_y_convertir(valor):
    """Convierte un texto en entero o flotante si es posible; de lo contrario, lo mantiene como cadena."""
    valor = valor.strip()
    try:
        return int(valor)
    except ValueError:
        pass
    try:
        return float(valor)
    except ValueError:
        pass
    return valor


def cargar_archivo(ruta):
    """Carga datos desde un archivo de texto separado por comas y retorna una lista de listas."""
    datos_procesados = []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea_limpia = linea.strip()
                if not linea_limpia:
                    continue  # Ignorar líneas vacías
                datos_fila = linea_limpia.split(",")
                fila_procesada = [evaluar_y_convertir(dato) for dato in datos_fila]
                datos_procesados.append(fila_procesada)
        return datos_procesados
    except Exception as e:
        print(f"Error inesperado al cargar el archivo '{ruta}': {e}")
        return []


def actualizar_archivo(ruta, datos):
    """Sobrescribe un archivo de texto con una lista de listas en formato separado por comas."""
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            for fila in datos:
                linea = ",".join(str(dato) for dato in fila) + "\n"
                archivo.write(linea)
    except Exception as e:
        print(f"Error inesperado al actualizar el archivo '{ruta}': {e}")