ruta_txt = "../datos/medicamentos.txt"

def inventario(ruta_archivo):
    datos_farmacos = []
    archivo_farmacos = open(ruta_archivo, "r")
    for linea in archivo_farmacos:
        farmaco = linea.strip().split(",")
        datos_farmacos.append(farmaco)
    archivo_farmacos.close()
    return datos_farmacos

def actualizar(ruta_archivo, inventario_cache):
    archivo_farmacos = open(ruta_archivo, "w")
    try:
        for farmaco, stock, precio in inventario_cache:
            archivo_farmacos.write(f"{farmaco},{stock},{precio}\n")
        print("Inventario guardado con exito")
        archivo_farmacos.close()
    except:
        print("Error en ruta del archivo")