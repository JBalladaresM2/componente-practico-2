libros=open('libros.txt', 'r')
nombre_txt=libros.name
mode_txt=libros.mode
print(f"El nombre del archivo es {nombre_txt} y el modo es {mode_txt}")
numero=5
print(libros.read(numero))
gps=libros.tell()
print(f"El cursor quedo en {gps}")
eli=seek(0)
print(f"rebobino en {eli}")
extraer=libros.readline()
print(f"Libros extraidos {extraer}")
try:
    libros.close()
    print("Libro cerrado exitosamente")
except:
    print("Error hijo de tu puta madre")