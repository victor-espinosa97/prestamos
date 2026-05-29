# ============================================================
# MODULO: prestamos.py
# DESCRIPCION: Prestamos, devoluciones, ventas y consultas
# ============================================================

import os
from datetime import datetime

# Impuesto que se cobra cuando alguien no devuelve el item a tiempo
IMPUESTO_CONCHUDEZ = 0.23


# ------------------------------------------------------------------
# Funcion auxiliar
# ------------------------------------------------------------------

def calcular_dias_transcurridos(fecha_inicio_str):
    """
    Recibe una fecha en formato texto y calcula cuantos dias han pasado
    desde esa fecha hasta hoy.
    """
    fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d %H:%M:%S")
    diferencia   = datetime.now() - fecha_inicio
    return diferencia.days


# ------------------------------------------------------------------
# 1. Registrar prestamo
# ------------------------------------------------------------------

def registrar_prestamo(usuarios, items, prestamos):
    """
    Registra un nuevo prestamo.
    - Verifica que el usuario exista por documento.
    - Muestra el inventario disponible.
    - El usuario elige el item por ID.
    """
    print("\n--- Registrar Nuevo Prestamo ---")

    # --- Buscar usuario por documento ---
    usuario = None
    while True:
        doc = input("Documento del usuario: ").strip()

        for u in usuarios:
            if u["doc"] == doc:
                usuario = u
                break

        if usuario is not None:
            print("  Usuario encontrado: " + usuario["nombre"] + " " + usuario["apellido"])
            break
        else:
            print("  ERROR: No existe un usuario con ese documento.")
            print("  Debe registrar al usuario antes de hacer un prestamo.")
            respuesta = input("  Desea intentar con otro documento? (s/n): ").strip().lower()
            if respuesta != "s":
                return

    # --- Mostrar inventario disponible ---
    disponibles = []
    for item in items:
        if item["disponible"] == True:
            disponibles.append(item)

    if len(disponibles) == 0:
        print("\n  No hay items disponibles en el inventario en este momento.")
        return

    print("\n  Inventario disponible:")
    print("  " + "-" * 50)
    print("  {:<12} {:<22} {:<14}".format("ID", "Nombre", "Categoria"))
    print("  " + "-" * 50)
    for item in disponibles:
        print("  {:<12} {:<22} {:<14}".format(
            item["id"],
            item["nombre"][:20],
            item["categoria"]
        ))
    print("  " + "-" * 50)

    # --- Seleccionar item por ID ---
    item_seleccionado = None
    while True:
        item_id = input("\n  Ingrese el ID del item a prestar: ").strip().upper()

        for item in disponibles:
            if item["id"] == item_id:
                item_seleccionado = item
                break

        if item_seleccionado is not None:
            print("  Item seleccionado: " + item_seleccionado["nombre"])
            break
        else:
            print("  ERROR: ID no valido o no disponible. Intente de nuevo.")

    # --- Crear el registro del prestamo ---
    fecha_ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    nuevo_prestamo = {
        "usuario_doc":    usuario["doc"],
        "usuario_nombre": usuario["nombre"] + " " + usuario["apellido"],
        "item_id":        item_seleccionado["id"],
        "item_nombre":    item_seleccionado["nombre"],
        "item_precio":    item_seleccionado["precio"],
        "fecha_inicio":   fecha_ahora,
        "dias_pactados":  usuario["tiempo"],
        "activo":         True
    }

    # Agregar prestamo a la lista
    prestamos.append(nuevo_prestamo)

    # Marcar el item como no disponible
    item_seleccionado["disponible"] = False

    # Sumar un prestamo al usuario
    usuario["prestamos_realizados"] = usuario["prestamos_realizados"] + 1

    print("\n  Prestamo registrado con exito!")
    print("  Usuario      : " + usuario["nombre"] + " " + usuario["apellido"])
    print("  Item         : " + item_seleccionado["nombre"])
    print("  Dias pactados: " + str(usuario["tiempo"]) + " dias")
    print("  Fecha inicio : " + fecha_ahora)


# ------------------------------------------------------------------
# 2. Registrar devolucion
# ------------------------------------------------------------------

def registrar_devolucion(prestamos, items):
    """
    Registra la devolucion de un prestamo activo.
    - Si el prestamo tiene mas de 30 dias, informa que debe procesarse como venta.
    - Si tiene menos de 30 dias, genera un certificado de devolucion en TXT.
    """
    print("\n--- Registrar Devolucion ---")

    doc = input("Documento del usuario: ").strip()

    # Buscar prestamos activos del usuario
    prestamos_activos = []
    for p in prestamos:
        if p["usuario_doc"] == doc and p["activo"] == True:
            prestamos_activos.append(p)

    if len(prestamos_activos) == 0:
        print("  El usuario no tiene prestamos activos.")
        print("  No se puede registrar la devolucion.")
        return

    # Mostrar prestamos activos del usuario
    print("\n  Prestamos activos del usuario:")
    for i in range(len(prestamos_activos)):
        p = prestamos_activos[i]
        dias = calcular_dias_transcurridos(p["fecha_inicio"])
        print("  " + str(i + 1) + ". " + p["item_nombre"] +
              " (ID: " + p["item_id"] + ") - " +
              str(dias) + " dias transcurridos")

    # Elegir cual prestamo devolver
    prestamo_elegido = None
    while True:
        entrada = input("\n  Seleccione el numero del prestamo a devolver: ").strip()

        if not entrada.isdigit():
            print("  ERROR: Ingrese un numero valido.")
            continue

        numero = int(entrada)

        if numero >= 1 and numero <= len(prestamos_activos):
            prestamo_elegido = prestamos_activos[numero - 1]
            break
        else:
            print("  ERROR: Numero fuera de rango. Intente de nuevo.")

    # Verificar si supero los 30 dias
    dias = calcular_dias_transcurridos(prestamo_elegido["fecha_inicio"])

    if dias > 30:
        print("\n  AVISO: Este prestamo supero los 30 dias permitidos.")
        print("  Use la opcion 4 del menu para procesar la venta automatica.")
        return

    # Procesar la devolucion normal
    prestamo_elegido["activo"] = False

    # Devolver el item al inventario
    for item in items:
        if item["id"] == prestamo_elegido["item_id"]:
            item["disponible"] = True
            break

    # Generar certificado TXT
    fecha_dev          = datetime.now().strftime("%Y-%m-%d")
    fecha_dev_completa = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Nombre del archivo: NombreUsuario_FechaDevolucion_IDItem.txt
    nombre_archivo  = prestamo_elegido["usuario_nombre"].replace(" ", "_")
    nombre_archivo  = nombre_archivo + "_" + fecha_dev + "_" + prestamo_elegido["item_id"] + ".txt"
    ruta_certificado = os.path.join("certificados", nombre_archivo)

    with open(ruta_certificado, "w", encoding="utf-8") as f:
        f.write("==========================================\n")
        f.write("       CERTIFICADO DE DEVOLUCION         \n")
        f.write("==========================================\n")
        f.write("Usuario      : " + prestamo_elegido["usuario_nombre"] + "\n")
        f.write("Documento    : " + prestamo_elegido["usuario_doc"] + "\n")
        f.write("Item         : " + prestamo_elegido["item_nombre"] + "\n")
        f.write("ID del item  : " + prestamo_elegido["item_id"] + "\n")
        f.write("Fecha inicio : " + prestamo_elegido["fecha_inicio"] + "\n")
        f.write("Fecha devol. : " + fecha_dev_completa + "\n")
        f.write("Dias usados  : " + str(dias) + " dias\n")
        f.write("==========================================\n")
        f.write("Estado: Devolucion Exitosa\n")
        f.write("==========================================\n")

    print("\n  Devolucion registrada con exito!")
    print("  Certificado generado: " + ruta_certificado)


# ------------------------------------------------------------------
# 3. Consultar items con mas de 30 dias (y generar ventas automaticas)
# ------------------------------------------------------------------

def consultar_y_procesar_morosos(prestamos, items, ventas):
    """
    Revisa todos los prestamos activos.
    Muestra los que tienen mas de 30 dias.
    Los convierte en ventas automaticamente y genera la factura TXT.
    """
    print("\n--- Items con mas de 30 dias de prestamo ---")

    # Buscar prestamos activos que superen los 30 dias
    morosos = []
    for p in prestamos:
        if p["activo"] == True:
            dias = calcular_dias_transcurridos(p["fecha_inicio"])
            if dias > 30:
                morosos.append(p)

    if len(morosos) == 0:
        print("  No hay prestamos que superen los 30 dias. Todo esta al dia.")
        return

    print("  Se encontraron " + str(len(morosos)) + " prestamo(s) con mora:\n")

    # Procesar cada prestamo moroso
    for p in morosos:
        dias     = calcular_dias_transcurridos(p["fecha_inicio"])
        subtotal = p["item_precio"]
        impuesto = subtotal * IMPUESTO_CONCHUDEZ
        total    = subtotal + impuesto

        print("  Usuario : " + p["usuario_nombre"])
        print("  Item    : " + p["item_nombre"] + " (ID: " + p["item_id"] + ")")
        print("  Dias    : " + str(dias) + " dias (supero 30)")
        print("  Subtotal: $" + "{:,.2f}".format(subtotal))
        print("  Impuesto conchudez 23%: $" + "{:,.2f}".format(impuesto))
        print("  TOTAL   : $" + "{:,.2f}".format(total))
        print("  " + "-" * 40)

        # Registrar la venta
        nueva_venta = {
            "usuario":    p["usuario_nombre"],
            "doc":        p["usuario_doc"],
            "item_id":    p["item_id"],
            "item_nombre": p["item_nombre"],
            "subtotal":   subtotal,
            "impuesto":   impuesto,
            "total":      total,
            "motivo":     "Excedio el tiempo maximo de prestamo (30 dias)"
        }
        ventas.append(nueva_venta)

        # Cerrar el prestamo
        p["activo"] = False

        # El item queda marcado como no disponible (fue vendido)
        for item in items:
            if item["id"] == p["item_id"]:
                item["disponible"] = False
                break

        # Generar factura TXT
        nombre_factura = p["usuario_nombre"].replace(" ", "_") + "_" + p["item_id"] + "_FACTURA.txt"
        ruta_factura   = os.path.join("facturas", nombre_factura)

        with open(ruta_factura, "w", encoding="utf-8") as f:
            f.write("==========================================\n")
            f.write("           FACTURA DE VENTA              \n")
            f.write("==========================================\n")
            f.write("Cliente  : " + nueva_venta["usuario"] + "\n")
            f.write("Producto : " + nueva_venta["item_nombre"] + " (ID: " + nueva_venta["item_id"] + ")\n")
            f.write("Motivo   : " + nueva_venta["motivo"] + "\n")
            f.write("------------------------------------------\n")
            f.write("Subtotal              : $" + "{:,.2f}".format(subtotal) + "\n")
            f.write("Impuesto Conchudez 23%: $" + "{:,.2f}".format(impuesto) + "\n")
            f.write("TOTAL A PAGAR         : $" + "{:,.2f}".format(total) + "\n")
            f.write("==========================================\n")

        print("  Venta registrada. Factura generada: " + ruta_factura)

    print("\n  Se procesaron " + str(len(morosos)) + " venta(s) automatica(s) por mora.")


# ------------------------------------------------------------------
# 4. Consultar estado general de prestamos activos
# ------------------------------------------------------------------

def consultar_estado_general(prestamos):
    """
    Muestra todos los prestamos activos ordenados de mayor a menor cantidad de dias.
    Guarda el reporte en un archivo de texto plano.
    """
    print("\n--- Consultar Articulos Prestados ---")

    # Filtrar solo los activos
    activos = []
    for p in prestamos:
        if p["activo"] == True:
            activos.append(p)

    if len(activos) == 0:
        print("  No hay prestamos activos para mostrar.")
        return

    # Calcular dias de cada prestamo y armar lista de reporte
    reporte = []
    for p in activos:
        dias = calcular_dias_transcurridos(p["fecha_inicio"])
        reporte.append({
            "id":      p["item_id"],
            "item":    p["item_nombre"],
            "usuario": p["usuario_nombre"],
            "dias":    dias
        })

    # Ordenar de mayor a menor dias (burbuja basico)
    for i in range(len(reporte)):
        for j in range(i + 1, len(reporte)):
            if reporte[j]["dias"] > reporte[i]["dias"]:
                temp       = reporte[i]
                reporte[i] = reporte[j]
                reporte[j] = temp

    # Mostrar en pantalla
    print("\n  {:<12} {:<22} {:<6} {}".format("ID", "Item", "Dias", "Usuario"))
    print("  " + "-" * 60)

    for r in reporte:
        print("  {:<12} {:<22} {:<6} {}".format(
            r["id"],
            r["item"][:20],
            str(r["dias"]),
            r["usuario"][:20]
        ))

    print("  " + "-" * 60)

    # Guardar reporte en archivo de texto
    os.makedirs("reportes", exist_ok=True)
    ruta_reporte  = os.path.join("reportes", "estado_prestamos.txt")
    fecha_reporte = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(ruta_reporte, "w", encoding="utf-8") as f:
        f.write("REPORTE DE ESTADO GENERAL - " + fecha_reporte + "\n")
        f.write("-" * 60 + "\n")
        f.write("{:<12} {:<22} {:<6} {}\n".format("ID", "Item", "Dias", "Usuario"))
        f.write("-" * 60 + "\n")
        for r in reporte:
            f.write("{:<12} {:<22} {:<6} {}\n".format(
                r["id"],
                r["item"][:20],
                str(r["dias"]),
                r["usuario"][:20]
            ))

    print("\n  Reporte guardado en: " + ruta_reporte)