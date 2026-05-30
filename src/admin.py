# admin.py
# Panel de administracion: login y reportes del sistema

import os
import items


def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


def login_admin():
    # Lista de usuarios y contrasenas permitidos
    credenciales = {
        "admin":      "1234",
        "lina.duque": "udea2026",
        "camila":     "udea2026"
    }

    print("\n" + "=" * 30)
    print("      ACCESO RESTRINGIDO")
    print("=" * 30)

    usuario = input("Usuario: ").strip()
    clave   = input("Contrasena: ").strip()

    if usuario in credenciales:
        if credenciales[usuario] == clave:
            print("  Acceso concedido. Bienvenido, " + usuario + "!")
            return True

    print("  ERROR: Usuario o contrasena incorrectos. Acceso denegado.")
    return False


# ------------------------------------------------------------------
# Reportes del panel de administracion
# ------------------------------------------------------------------

def mostrar_metricas(prestamos, ventas):
    # Muestra el resumen general de numeros del sistema
    total_prestamos = len(prestamos)

    total_devueltos = 0
    for p in prestamos:
        if p["activo"] == False:
            total_devueltos = total_devueltos + 1

    total_ventas = len(ventas)

    recaudo = 0
    for v in ventas:
        recaudo = recaudo + v["total"]

    print("\n  --- METRICAS GENERALES DEL SISTEMA ---")
    print("  Total de prestamos registrados : " + str(total_prestamos))
    print("  Total de items devueltos       : " + str(total_devueltos))
    print("  Total de ventas realizadas     : " + str(total_ventas))
    print("  Total recaudado (ventas)       : $" + "{:,.2f}".format(recaudo))


def mostrar_lista_usuarios(usuarios):
    # Muestra todos los usuarios registrados en el sistema
    if len(usuarios) == 0:
        print("\n  No hay usuarios registrados.")
        return

    print("\n  --- LISTA DE USUARIOS REGISTRADOS ---")
    print("  {:<15} {:<25} {:<10}".format("Documento", "Nombre completo", "Prestamos"))
    print("  " + "-" * 55)

    for u in usuarios:
        nombre_completo = u["nombre"] + " " + u["apellido"]
        print("  {:<15} {:<25} {:<10}".format(
            u["doc"],
            nombre_completo[:24],
            str(u["prestamos_realizados"])
        ))


def mostrar_extremos_usuarios(usuarios):
    # Muestra quien tiene mas y quien tiene menos prestamos
    if len(usuarios) == 0:
        print("\n  No hay usuarios para analizar.")
        return

    usuario_mayor = usuarios[0]
    usuario_menor = usuarios[0]

    for u in usuarios:
        if u["prestamos_realizados"] > usuario_mayor["prestamos_realizados"]:
            usuario_mayor = u
        if u["prestamos_realizados"] < usuario_menor["prestamos_realizados"]:
            usuario_menor = u

    print("\n  --- USUARIOS DESTACADOS ---")
    print("  Mayor cantidad de prestamos:")
    print("    Nombre    : " + usuario_mayor["nombre"] + " " + usuario_mayor["apellido"])
    print("    Documento : " + usuario_mayor["doc"])
    print("    Prestamos : " + str(usuario_mayor["prestamos_realizados"]))

    print("\n  Menor cantidad de prestamos:")
    print("    Nombre    : " + usuario_menor["nombre"] + " " + usuario_menor["apellido"])
    print("    Documento : " + usuario_menor["doc"])
    print("    Prestamos : " + str(usuario_menor["prestamos_realizados"]))


# ------------------------------------------------------------------
# Menu del panel de administracion
# ------------------------------------------------------------------

def menu_admin(usuarios, list_items, prestamos, ventas):
    while True:
        print("\n" + "=" * 42)
        print("      PANEL DE ADMINISTRACION")
        print("=" * 42)
        print("  1. Ver metricas generales")
        print("  2. Ver lista de usuarios")
        print("  3. Ver usuario con mas y menos prestamos")
        print("  4. Registrar nuevo item")
        print("  0. Volver al menu principal")
        print("=" * 42)

        opcion = input("  Seleccione una opcion: ").strip()

        if opcion == "1":
            limpiar_pantalla()
            mostrar_metricas(prestamos, ventas)

        elif opcion == "2":
            limpiar_pantalla()
            mostrar_lista_usuarios(usuarios)

        elif opcion == "3":
            limpiar_pantalla()
            mostrar_extremos_usuarios(usuarios)

        elif opcion == "4":
            limpiar_pantalla()
            items.registrar_item(list_items)

        elif opcion == "0":
            print("  Saliendo del panel administrativo...")
            break

        else:
            print("  ERROR: Opcion no valida. Intente de nuevo.")

        input("\n  Presione Enter para continuar...")
        limpiar_pantalla()