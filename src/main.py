import os
import usuarios
import items


def asegurar_entorno():
    """
    Garantiza que existan todas las carpetas necesarias
    antes de empezar a trabajar con archivos.
    """
    carpetas = ["data", "certificados", "reportes", "facturas"]
    for carpeta in carpetas:
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)


def limpiar_pantalla():
    """Limpia la consola para mejorar la experiencia de usuario."""
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_principal():
    """
    Función principal que orquesta toda la aplicación.
    Carga los datos al inicio, los mantiene en memoria
    y cada módulo guarda de manera inmediata sus cambios.
    """
    # 1. Preparar carpetas del proyecto
    asegurar_entorno()

    # 2. Cargar todos los datos en memoria al arrancar
    list_usuarios  = []
    list_items     = []

    # 4. Ciclo principal del menú
    while True:
        limpiar_pantalla()
        print("===========================================")
        print("        SISTEMA DATA FILE SOLUTION        ")
        print("      Gestion Eficiente de Activos        ")
        print("===========================================")
        print("  1. Registrar Usuario")
        print("  2. Registrar Item (objeto a prestar)")
        print("  3. Registrar Prestamo")
        print("  4. Registrar y Certificar Devolucion")
        print("  5. Consultar Estado General de Prestamos")
        print("  6. Panel de Administracion")
        print("  0. Salir")
        print("===========================================")

        opcion = input("  Seleccione una opcion: ").strip()

        if opcion == "1":
            limpiar_pantalla()
            usuarios.registrar_usuario(list_usuarios)

        elif opcion == "2":
            limpiar_pantalla()
            items.registrar_item(list_items)

        elif opcion == "3":
            limpiar_pantalla()
            print("Registrar Prestamo(Pendiente)")

        elif opcion == "4":
            limpiar_pantalla()
            print("Registrar y Certificar Devolucion(Pendiente)")

        elif opcion == "5":
            limpiar_pantalla()
            print("Consultar Estado General de Prestamos(Pendiente)")

        elif opcion == "6":
            limpiar_pantalla()
            print("Panel de Administracion(Pendiente)")

        elif opcion == "0":
            print("\n  Hasta pronto!")
            break

        else:
            print("\n  ERROR: Opcion no valida. Intente con un numero del 0 al 6.")

        # Pausa solo si no se eligió salir
        if opcion != "0":
            input("\n  Presione Enter para continuar...")


# Punto de entrada del programa
if __name__ == "__main__":
    menu_principal()