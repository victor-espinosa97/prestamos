# main.py
# Archivo principal del sistema Data File Solution
# Desde aqui se inicia todo el programa

import os
import csv
import usuarios
import items
import prestamos
import admin


def limpiar_pantalla():
    # Limpia la consola para que el menu se vea ordenado
    os.system('cls' if os.name == 'nt' else 'clear')


def crear_carpetas():
    # Crea las carpetas que el programa necesita para guardar archivos
    # Si ya existen no pasa nada, las ignora
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists("certificados"):
        os.makedirs("certificados")
    if not os.path.exists("facturas"):
        os.makedirs("facturas")
    if not os.path.exists("reportes"):
        os.makedirs("reportes")


def cargar_usuarios():
    # Lee data/usuarios.csv y devuelve la lista de usuarios
    # Si el archivo no existe devuelve una lista vacia
    lista = []
    ruta  = os.path.join("data", "usuarios.csv")

    if not os.path.exists(ruta):
        return lista

    with open(ruta, "r", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector)  # Saltar la fila de encabezados

        for fila in lector:
            # Columnas: fecha_registro, documento, nombre, apellido, correo, dias_prestamo
            usuario = {
                "doc":                  fila[1],
                "nombre":               fila[2],
                "apellido":             fila[3],
                "correo":               fila[4],
                "tiempo":               int(fila[5]),
                "prestamos_realizados": 0
            }
            lista.append(usuario)

    print("  Usuarios cargados: " + str(len(lista)))
    return lista


def cargar_items():
    # Lee data/items.csv y devuelve la lista de items
    # Si el archivo no existe devuelve una lista vacia
    lista = []
    ruta  = os.path.join("data", "items.csv")

    if not os.path.exists(ruta):
        return lista

    with open(ruta, "r", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector)  # Saltar encabezados

        for fila in lector:
            # Columnas: fecha_registro, id, nombre, categoria, precio, estado
            item = {
                "id":         fila[1],
                "nombre":     fila[2],
                "categoria":  fila[3],
                "precio":     float(fila[4]),
                "estado":     fila[5],
                "disponible": True  # Se corrige abajo al revisar prestamos activos
            }
            lista.append(item)

    print("  Items cargados: " + str(len(lista)))
    return lista


def cargar_prestamos():
    # Lee data/prestamos.csv y devuelve la lista de prestamos
    # Todos se cargan como activos al principio, luego se corrigen
    # Si el archivo no existe devuelve una lista vacia
    lista = []
    ruta  = os.path.join("data", "prestamos.csv")

    if not os.path.exists(ruta):
        return lista

    with open(ruta, "r", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector)  # Saltar encabezados

        for fila in lector:
            # Columnas: fecha_registro, usuario, documento, item_id, item_nombre, precio, dias_pactados, fecha_inicio
            prestamo = {
                "usuario_doc":    fila[2],
                "usuario_nombre": fila[1],
                "item_id":        fila[3],
                "item_nombre":    fila[4],
                "item_precio":    float(fila[5]),
                "dias_pactados":  int(fila[6]),
                "fecha_inicio":   fila[7],
                "activo":         True  # Se corrige abajo al revisar devoluciones y ventas
            }
            lista.append(prestamo)

    print("  Prestamos cargados: " + str(len(lista)))
    return lista


def cargar_ventas(list_prestamos, list_usuarios, list_items):
    # Lee devoluciones.csv y ventas.csv para saber cuales prestamos ya cerraron
    # Tambien corrige el campo disponible de los items y prestamos_realizados de usuarios
    # Devuelve la lista de ventas para que el panel admin pueda mostrar las metricas

    # Marcar prestamos que ya fueron devueltos
    ruta_dev = os.path.join("data", "devoluciones.csv")
    if os.path.exists(ruta_dev):
        with open(ruta_dev, "r", encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            next(lector)
            for fila in lector:
                # Columnas: fecha_devolucion, usuario, documento, item_id, item_nombre, dias_usados
                doc_buscado  = fila[2]
                item_buscado = fila[3]
                for p in list_prestamos:
                    if p["usuario_doc"] == doc_buscado and p["item_id"] == item_buscado and p["activo"] == True:
                        p["activo"] = False
                        break

    # Marcar prestamos que se convirtieron en venta y reconstruir lista de ventas
    list_ventas  = []
    ruta_ventas  = os.path.join("data", "ventas.csv")
    if os.path.exists(ruta_ventas):
        with open(ruta_ventas, "r", encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            next(lector)
            for fila in lector:
                # Columnas: fecha, usuario, documento, item_id, item_nombre, subtotal, impuesto, total
                doc_buscado  = fila[2]
                item_buscado = fila[3]
                for p in list_prestamos:
                    if p["usuario_doc"] == doc_buscado and p["item_id"] == item_buscado and p["activo"] == True:
                        p["activo"] = False
                        break

                venta = {
                    "usuario":    fila[1],
                    "doc":        fila[2],
                    "item_id":    fila[3],
                    "item_nombre": fila[4],
                    "subtotal":   float(fila[5]),
                    "impuesto":   float(fila[6]),
                    "total":      float(fila[7]),
                    "motivo":     "Excedio el tiempo maximo de prestamo (30 dias)"
                }
                list_ventas.append(venta)

    # Con los prestamos ya corregidos, marcar los items que siguen prestados como no disponibles
    for p in list_prestamos:
        if p["activo"] == True:
            for item in list_items:
                if item["id"] == p["item_id"]:
                    item["disponible"] = False
                    break

    # Recalcular cuantos prestamos ha hecho cada usuario
    for p in list_prestamos:
        for u in list_usuarios:
            if u["doc"] == p["usuario_doc"]:
                u["prestamos_realizados"] = u["prestamos_realizados"] + 1
                break

    print("  Ventas cargadas: " + str(len(list_ventas)))
    return list_ventas


def menu_principal():

    crear_carpetas()

    # Cargar todos los datos guardados en los CSV al arrancar
    print("\n  Cargando datos guardados...")
    list_usuarios  = cargar_usuarios()
    list_items     = cargar_items()
    list_prestamos = cargar_prestamos()
    list_ventas    = cargar_ventas(list_prestamos, list_usuarios, list_items)
    print("  Listo.\n")

    # Ciclo principal del menu
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

        if opcion == "1":
            limpiar_pantalla()
            usuarios.registrar_usuario(list_usuarios)

        elif opcion == "2":
            limpiar_pantalla()
            prestamos.registrar_prestamo(list_usuarios, list_items, list_prestamos)

        elif opcion == "3":
            limpiar_pantalla()
            prestamos.registrar_devolucion(list_prestamos, list_items)

        elif opcion == "4":
            limpiar_pantalla()
            prestamos.consultar_y_procesar_morosos(list_prestamos, list_items, list_ventas)

        elif opcion == "5":
            limpiar_pantalla()
            prestamos.consultar_estado_general(list_prestamos)

        elif opcion == "6":
            limpiar_pantalla()
            if admin.login_admin():
                admin.menu_admin(list_usuarios, list_items, list_prestamos, list_ventas)

        elif opcion == "0":
            print("\n  Hasta pronto!")
            break

        else:
            print("\n  ERROR: Opcion no valida. Ingrese un numero del 0 al 6.")

        if opcion != "0":
            input("\n  Presione Enter para continuar...")


menu_principal()