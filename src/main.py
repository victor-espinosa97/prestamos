# ============================================================
# ARCHIVO PRINCIPAL: main.py
# DESCRIPCION: Punto de entrada del sistema Data File Solution
#              Orquesta todos los modulos del programa
# ============================================================

import os
import admin
import prestamos
import usuarios
import items


def asegurar_carpetas():
    """
    Crea las carpetas necesarias si no existen todavia.
    certificados/ -> donde se guardan los TXT de devolucion
    reportes/     -> donde se guarda el estado de prestamos
    facturas/     -> donde se guardan las facturas de venta
    """
    carpetas = ["certificados", "reportes", "facturas"]
    for carpeta in carpetas:
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)


def limpiar_pantalla():
    """Limpia la consola para mejorar la experiencia de usuario."""
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_principal():
    """
    Funcion principal que controla todo el programa.
    - Carga los datos en memoria al arrancar.
    - Muestra el menu principal en un bucle.
    - Llama al modulo correspondiente segun la opcion elegida.
    """

    # 1. Crear las carpetas del proyecto si no existen
    asegurar_carpetas()

    # 2. Datos iniciales de prueba
    #    Estos datos ya estan cargados para poder probar el programa
    #    desde el primer momento sin necesidad de registrar todo manualmente.

    list_usuarios = [
        {
            "doc":                  "1020304050",
            "nombre":               "Lina",
            "apellido":             "Duque",
            "correo":               "lina@gmail.com",
            "tiempo":               15,
            "prestamos_realizados": 1
        }
    ]

    list_items = [
        {
            "id":         "TEC-001",
            "nombre":     "Laptop ASUS ROG Strix",
            "categoria":  "Miscelaneo",
            "precio":     1500.00,
            "estado":     "Excelente (Como nuevo)",
            "disponible": False   # False porque esta prestado actualmente
        }
    ]

    # NOTA: La fecha de inicio esta puesta en el pasado (mas de 30 dias atras)
    # para que puedas probar la opcion 4 (ventas automaticas) desde el primer momento.
    list_prestamos = [
        {
            "usuario_doc":    "1020304050",
            "usuario_nombre": "Lina Duque",
            "item_id":        "TEC-001",
            "item_nombre":    "Laptop ASUS ROG Strix",
            "item_precio":    1500.00,
            "fecha_inicio":   "2026-04-10 14:30:00",  # Hace mas de 30 dias
            "dias_pactados":  15,
            "activo":         True
        }
    ]

    list_ventas = []

    # 3. Ciclo principal del menu
    while True:
        limpiar_pantalla()
        print("===========================================")
        print("        SISTEMA DATA FILE SOLUTION        ")
        print("      Gestion Eficiente de Activos        ")
        print("===========================================")
        print("  1. Registrar Usuario")
        print("  2. Registrar Prestamo")
        print("  3. Registrar Devolucion")
        print("  4. Consultar items con mas de 30 dias")
        print("  5. Consultar articulos prestados")
        print("  6. Administrador")
        print("  0. Salir")
        print("===========================================")

        opcion = input("  Seleccione una opcion: ").strip()

        # Opcion 1: Registrar un nuevo usuario
        if opcion == "1":
            limpiar_pantalla()
            usuarios.registrar_usuario(list_usuarios)

        # Opcion 2: Registrar un nuevo prestamo
        elif opcion == "2":
            limpiar_pantalla()
            prestamos.registrar_prestamo(list_usuarios, list_items, list_prestamos)

        # Opcion 3: Registrar devolucion de un prestamo activo
        elif opcion == "3":
            limpiar_pantalla()
            prestamos.registrar_devolucion(list_prestamos, list_items)

        # Opcion 4: Ver items con mas de 30 dias y generar ventas automaticas
        elif opcion == "4":
            limpiar_pantalla()
            prestamos.consultar_y_procesar_morosos(list_prestamos, list_items, list_ventas)

        # Opcion 5: Ver todos los articulos actualmente prestados
        elif opcion == "5":
            limpiar_pantalla()
            prestamos.consultar_estado_general(list_prestamos)

        # Opcion 6: Panel de administracion (requiere usuario y contrasena)
        elif opcion == "6":
            limpiar_pantalla()
            if admin.login_admin():
                admin.menu_admin(list_usuarios, list_items, list_prestamos, list_ventas)

        # Opcion 0: Salir del programa
        elif opcion == "0":
            print("\n  Hasta pronto!")
            break

        else:
            print("\n  ERROR: Opcion no valida. Ingrese un numero del 0 al 6.")

        # Pausa para que el usuario lea el resultado antes de limpiar la pantalla
        if opcion != "0":
            input("\n  Presione Enter para continuar...")


# Punto de entrada del programa
# Este bloque solo se ejecuta si corres main.py directamente
if __name__ == "__main__":
    menu_principal()