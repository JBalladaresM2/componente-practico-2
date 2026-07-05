def inventario() :
 medicamentos = open("datos/medicamentos.txt" , "r") 
 lista=[]
 for linea in medicamentos:
        medicamento=linea.strip().split(",")
        nombre=medicamento[0]
        cantidad=int(medicamento[1])
        precio=float(medicamento[2])
        lista.append((nombre , cantidad , precio))
        medicamentos.close()
 return lista 
def cambio(lista_nueva):
 medicamentos = open("datos/medicamentos.txt" , "w")
 for linea in medicamentos:
    nombre, cantidad, precio = linea
    linea=f"{nombre},{cantidad},{precio}\n"
    medicamentos.write(linea)
    return(print("Inventario guardado con exito"))


