def inventario():
    datos_farmacos = []
    try:
       archivo_farmacos = open("../datos/medicamentos.txt", "r")
       for linea in archivo_farmacos:
              farmaco = linea.strip().split(",")
              datos_farmacos.append(farmaco)
       archivo_farmacos.close()
       return datos_farmacos
    except:
        print("Error en ruta del archivo")

def actualizar(inventario_cache):
    try:
        archivo_farmacos = open("../datos/medicamentos.txt", "w") 
        for farmaco, stock, precio in inventario_cache:
            archivo_farmacos.write(f"{farmaco},{stock},{precio}\n")
        print("Inventario guardado con exito")
        archivo_farmacos.close()
    except:
        print("Error en ruta del archivo")