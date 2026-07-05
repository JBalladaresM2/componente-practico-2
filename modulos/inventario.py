medicamentos = open("datos/medicamentos.txt" , "r")
inventario = [
]
lista=[]
for linea in medicamentos:
    medicamento=linea.strip().split(",")
    print(medicamento)
    nombre=medicamento[0]
    cantidad=int(medicamento[1])
    lista.append((nombre , cantidad))
print(lista)



 