#../modulos/inventario.py
def inventario(ruta):#Funcion que crea la lista a traves de un archivo de texto
    datos_farmacos = []#Se crea la variable datos_farmacos , la cual tomara el rol de lista
    try:#Busca un error en el codigo
       archivo_farmacos = open(ruta, "r")#Busca el archivo de texto , lo abre y lo guarda en la variable archivo_farmacos
       for linea in archivo_farmacos:#Recorre el archivo linea por linea
              medicamento, stock, precio = linea.strip().split(",")#Agarra la linea , luego borra los saltos de linea y separa la linea cuando llega a una coma en dos formando una tupla
              datos_farmacos.append([medicamento, int(stock), float(precio)])#Se guarda la tupla en el arreglo
       archivo_farmacos.close()#Se cierra el archivo correctamente
       return datos_farmacos#Retorna el arreglo
    except:#Si hay un error sale el siguiente mensaje
        print("Error en ruta del archivo")#Imprime este mensaje por si sale un error en la ruta de archivo

def actualizar(ruta, inventario_cache):#Funcion que actualiza el archivo de texto
    try:#Busca un error en el codigo
        archivo_farmacos = open(ruta, "w")#Abre el archivo de texto y lo empieza a escribir
        for farmaco, stock, precio in inventario_cache:#Recorre cada item de la lista
            archivo_farmacos.write(f"{farmaco},{stock},{precio}\n")#Escribe cada elemento de la lista en el archivo txt
        print("Inventario guardado con exito")#Se imprime el mensaje que el inventario fue guardado correctamente
        archivo_farmacos.close()#Se cierra el archivo correctamente
    except:#Si encuentra un error , sigue la linea de codigo de abajo
        print("Error en ruta del archivo")#Imprime este mensaje por si sale un error en la ruta del archivo