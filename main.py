"""Punto de entrada principal del Sistema de Farmacia - Grupo 7.

Este script inicia la aplicación, realiza la carga directa del inventario
y pedidos desde los archivos de persistencia hacia las clases, y ejecuta
el bucle principal del menú de consola.
"""

import os
from clases.medicamento import Medicamento
from modulos.gestion_archivos import cargar_archivo
from modulos.menus import (
    RUTA_INV_MED,
    RUTA_REG_PED,
    mostrar_menu_principal,
    menu_registrar,
    menu_consultar,
    menu_buscar,
    menu_actualizar,
    menu_eliminar,
    menu_crear_pedido,
    menu_consultar_pedidos,
)


def main():
    """Función principal que ejecuta el ciclo de vida del sistema de farmacia."""
    # 1. Comunicación directa: se cargan filas del archivo y las clases asumen su importación
    medicamentos = [Medicamento.desde_lista(fila) for fila in cargar_archivo(RUTA_INV_MED)]
    historial_pedidos = cargar_archivo(RUTA_REG_PED)

    # 2. Bucle principal de interacción por consola
    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ").strip()
        os.system("cls")

        if opcion == "1":
            menu_registrar(medicamentos)
        elif opcion == "2":
            menu_actualizar(medicamentos)
        elif opcion == "3":
            menu_buscar(medicamentos)
        elif opcion == "4":
            menu_consultar(medicamentos)
        elif opcion == "5":
            menu_eliminar(medicamentos)
        elif opcion == "6":
            menu_crear_pedido(medicamentos, historial_pedidos)
        elif opcion == "7":
            menu_consultar_pedidos(historial_pedidos)
        elif opcion == "8":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida, intente nuevamente.")


if __name__ == "__main__":
    os.system("cls")
    main()
