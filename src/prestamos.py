# prestamos.py
# Manejo de prestamos, devoluciones, ventas por mora y consultas

import os
import csv
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# El impuesto que se cobra si alguien no devuelve el item a tiempo
IMPUESTO_CONCHUDEZ = 0.23


# ------------------------------------------------------------------
# Funcion auxiliar para calcular dias
# ------------------------------------------------------------------

def calcular_dias_transcurridos(fecha_inicio_str):
    # Recibe una fecha en texto y calcula cuantos dias han pasado hasta hoy
    fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d %H:%M:%S")
    diferencia   = datetime.now() - fecha_inicio
    return diferencia.days


# ------------------------------------------------------------------
# Funciones para guardar en CSV
# ------------------------------------------------------------------

def guardar_prestamo_en_csv(prestamo):
    # Guarda el prestamo en data/prestamos.csv
    ruta           = os.path.join("data", "prestamos.csv")
    archivo_existe = os.path.exists(ruta)

    with open(ruta, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)

        if not archivo_existe:
            escritor.writerow(["fecha_registro", "usuario", "documento", "item_id", "item_nombre", "precio", "dias_pactados", "fecha_inicio"])

        escritor.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            prestamo["usuario_nombre"],
            prestamo["usuario_doc"],
            prestamo["item_id"],
            prestamo["item_nombre"],
            "{:.2f}".format(prestamo["item_precio"]),
            str(prestamo["dias_pactados"]),
            prestamo["fecha_inicio"]
        ])

    print("  Prestamo guardado en data/prestamos.csv")


def guardar_devolucion_en_csv(prestamo, dias):
    # Guarda la devolucion en data/devoluciones.csv
    ruta           = os.path.join("data", "devoluciones.csv")
    archivo_existe = os.path.exists(ruta)

    with open(ruta, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)

        if not archivo_existe:
            escritor.writerow(["fecha_devolucion", "usuario", "documento", "item_id", "item_nombre", "dias_usados"])

        escritor.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            prestamo["usuario_nombre"],
            prestamo["usuario_doc"],
            prestamo["item_id"],
            prestamo["item_nombre"],
            str(dias)
        ])

    print("  Devolucion guardada en data/devoluciones.csv")


def guardar_venta_en_csv(venta):
    # Guarda la venta en data/ventas.csv
    ruta           = os.path.join("data", "ventas.csv")
    archivo_existe = os.path.exists(ruta)

    with open(ruta, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)

        if not archivo_existe:
            escritor.writerow(["fecha", "usuario", "documento", "item_id", "item_nombre", "subtotal", "impuesto", "total"])

        escritor.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            venta["usuario"],
            venta["doc"],
            venta["item_id"],
            venta["item_nombre"],
            "{:.2f}".format(venta["subtotal"]),
            "{:.2f}".format(venta["impuesto"]),
            "{:.2f}".format(venta["total"])
        ])

    print("  Venta guardada en data/ventas.csv")


# ------------------------------------------------------------------
# Funciones para generar PDFs
# ------------------------------------------------------------------

# Genera el certificado de devolucion en formato PDF
def generar_pdf_certificado(prestamo, dias, ruta_pdf):
    c           = canvas.Canvas(ruta_pdf, pagesize=letter)
    ancho, alto = letter
    margen      = 50
    y           = alto - 60

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(ancho / 2, y, "DATA FILE SOLUTION")
    y -= 22

    c.setFont("Helvetica", 11)
    c.drawCentredString(ancho / 2, y, "Gestion Eficiente de Activos")
    y -= 15

    c.line(margen, y, ancho - margen, y)
    y -= 20

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(ancho / 2, y, "CERTIFICADO DE DEVOLUCION")
    y -= 30

    c.setFont("Helvetica", 10)
    c.drawString(margen, y, "Fecha: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    y -= 25

    c.line(margen, y, ancho - margen, y)
    y -= 20

    c.setFont("Helvetica-Bold", 11)
    c.drawString(margen, y, "DATOS DEL USUARIO")
    y -= 16

    c.setFont("Helvetica", 11)
    c.drawString(margen, y, "Nombre    : " + prestamo["usuario_nombre"])
    y -= 15
    c.drawString(margen, y, "Documento : " + prestamo["usuario_doc"])
    y -= 22

    c.line(margen, y, ancho - margen, y)
    y -= 20

    c.setFont("Helvetica-Bold", 11)
    c.drawString(margen, y, "DATOS DEL ARTICULO")
    y -= 16

    c.setFont("Helvetica", 11)
    c.drawString(margen, y, "Articulo    : " + prestamo["item_nombre"])
    y -= 15
    c.drawString(margen, y, "ID          : " + prestamo["item_id"])
    y -= 15
    c.drawString(margen, y, "Fecha inicio: " + prestamo["fecha_inicio"])
    y -= 15
    c.drawString(margen, y, "Dias usados : " + str(dias) + " dias")
    y -= 28

    c.line(margen, y, ancho - margen, y)
    y -= 22

    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(ancho / 2, y, "ESTADO: DEVOLUCION EXITOSA")

    c.save()
    print("  Certificado PDF generado: " + ruta_pdf)


def generar_pdf_factura(venta, ruta_pdf):
    # Genera la factura de venta en formato PDF
    c           = canvas.Canvas(ruta_pdf, pagesize=letter)
    ancho, alto = letter
    margen      = 50
    y           = alto - 60

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(ancho / 2, y, "DATA FILE SOLUTION")
    y -= 22

    c.setFont("Helvetica", 11)
    c.drawCentredString(ancho / 2, y, "Gestion Eficiente de Activos")
    y -= 15

    c.line(margen, y, ancho - margen, y)
    y -= 20

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(ancho / 2, y, "FACTURA DE VENTA")
    y -= 30

    c.setFont("Helvetica", 10)
    c.drawString(margen, y, "Fecha: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    y -= 25

    c.line(margen, y, ancho - margen, y)
    y -= 20

    c.setFont("Helvetica-Bold", 11)
    c.drawString(margen, y, "DATOS DEL CLIENTE")
    y -= 16

    c.setFont("Helvetica", 11)
    c.drawString(margen, y, "Cliente   : " + venta["usuario"])
    y -= 15
    c.drawString(margen, y, "Documento : " + venta["doc"])
    y -= 22

    c.line(margen, y, ancho - margen, y)
    y -= 20

    c.setFont("Helvetica-Bold", 11)
    c.drawString(margen, y, "ARTICULO")
    y -= 16

    c.setFont("Helvetica", 11)
    c.drawString(margen, y, "Producto : " + venta["item_nombre"])
    y -= 15
    c.drawString(margen, y, "ID       : " + venta["item_id"])
    y -= 15
    c.drawString(margen, y, "Motivo   : " + venta["motivo"])
    y -= 22

    c.line(margen, y, ancho - margen, y)
    y -= 20

    c.setFont("Helvetica-Bold", 11)
    c.drawString(margen, y, "RESUMEN DE PAGO")
    y -= 18

    c.setFont("Helvetica", 11)
    c.drawString(margen, y, "Subtotal              :")
    c.drawRightString(ancho - margen, y, "$" + "{:,.2f}".format(venta["subtotal"]))
    y -= 15

    c.drawString(margen, y, "Impuesto conchudez 23%:")
    c.drawRightString(ancho - margen, y, "$" + "{:,.2f}".format(venta["impuesto"]))
    y -= 8

    c.line(margen, y, ancho - margen, y)
    y -= 16

    c.setFont("Helvetica-Bold", 12)
    c.drawString(margen, y, "TOTAL A PAGAR         :")
    c.drawRightString(ancho - margen, y, "$" + "{:,.2f}".format(venta["total"]))

    c.save()
    print("  Factura PDF generada: " + ruta_pdf)


# ------------------------------------------------------------------
# Opcion 2: Registrar prestamo
# ------------------------------------------------------------------

def registrar_prestamo(usuarios, items, prestamos):
    print("\n--- Registrar Nuevo Prestamo ---")

    # Buscar al usuario por documento
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

    # Mostrar solo los items que estan disponibles
    disponibles = []
    for item in items:
        if item["disponible"] == True:
            disponibles.append(item)

    if len(disponibles) == 0:
        print("\n  No hay items disponibles en este momento.")
        return

    print("\n  Inventario disponible:")
    print("  " + "-" * 50)
    print("  {:<12} {:<22} {:<14}".format("ID", "Nombre", "Categoria"))
    print("  " + "-" * 50)
    for item in disponibles:
        print("  {:<12} {:<22} {:<14}".format(item["id"], item["nombre"][:20], item["categoria"]))
    print("  " + "-" * 50)

    # El usuario elige el item por ID
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

    # Preguntar si quiere usar la fecha de hoy o ingresar una manualmente
    # Util para simular prestamos con mas de 30 dias sin esperar
    print("\n  Fecha de inicio del prestamo:")
    print("  1. Usar la fecha de hoy")
    print("  2. Ingresar una fecha manualmente")
    opcion_fecha = input("  Seleccione una opcion: ").strip()

    if opcion_fecha == "2":
        fecha_ahora = ""
        while True:
            entrada = input("  Ingrese la fecha (formato: YYYY-MM-DD, ej: 2026-01-15): ").strip()

            # Verificar que tenga el formato correcto intentando convertirla
            try:
                datetime.strptime(entrada, "%Y-%m-%d")
                # Si llega aqui es porque la fecha es valida
                fecha_ahora = entrada + " 00:00:00"
                break
            except ValueError:
                print("  ERROR: Fecha invalida. Use el formato YYYY-MM-DD (ej: 2026-01-15).")
    else:
        fecha_ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Crear el registro del prestamo

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

    prestamos.append(nuevo_prestamo)
    item_seleccionado["disponible"] = False
    usuario["prestamos_realizados"] = usuario["prestamos_realizados"] + 1

    # Guardar en CSV
    guardar_prestamo_en_csv(nuevo_prestamo)

    print("\n  Prestamo registrado con exito!")
    print("  Item         : " + item_seleccionado["nombre"])
    print("  Dias pactados: " + str(usuario["tiempo"]) + " dias")
    print("  Fecha inicio : " + fecha_ahora)


# ------------------------------------------------------------------
# Opcion 3: Registrar devolucion
# ------------------------------------------------------------------

def registrar_devolucion(prestamos, items):
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

    # Mostrar los prestamos activos del usuario
    print("\n  Prestamos activos del usuario:")
    for i in range(len(prestamos_activos)):
        p    = prestamos_activos[i]
        dias = calcular_dias_transcurridos(p["fecha_inicio"])
        print("  " + str(i + 1) + ". " + p["item_nombre"] +
              " (ID: " + p["item_id"] + ") - " + str(dias) + " dias transcurridos")

    # El usuario elige cual devolver
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

    dias = calcular_dias_transcurridos(prestamo_elegido["fecha_inicio"])

    # Si supero 30 dias no se puede devolver, debe procesarse como venta
    if dias > 30:
        print("\n  AVISO: Este prestamo supero los 30 dias permitidos.")
        print("  Use la opcion 4 del menu para procesar la venta automatica.")
        return

    # Marcar el prestamo como cerrado
    prestamo_elegido["activo"] = False

    # Devolver el item al inventario
    for item in items:
        if item["id"] == prestamo_elegido["item_id"]:
            item["disponible"] = True
            break

    # Nombre base para los archivos que se van a generar
    fecha_dev   = datetime.now().strftime("%Y-%m-%d")
    nombre_base = prestamo_elegido["usuario_nombre"].replace(" ", "_")
    nombre_base = nombre_base + "_" + fecha_dev + "_" + prestamo_elegido["item_id"]

    # Generar certificado TXT
    ruta_txt = os.path.join("certificados", nombre_base + ".txt")

    with open(ruta_txt, "w", encoding="utf-8") as f:
        f.write("==========================================\n")
        f.write("       CERTIFICADO DE DEVOLUCION         \n")
        f.write("==========================================\n")
        f.write("Usuario      : " + prestamo_elegido["usuario_nombre"] + "\n")
        f.write("Documento    : " + prestamo_elegido["usuario_doc"] + "\n")
        f.write("Item         : " + prestamo_elegido["item_nombre"] + "\n")
        f.write("ID del item  : " + prestamo_elegido["item_id"] + "\n")
        f.write("Fecha inicio : " + prestamo_elegido["fecha_inicio"] + "\n")
        f.write("Fecha devol. : " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        f.write("Dias usados  : " + str(dias) + " dias\n")
        f.write("==========================================\n")
        f.write("Estado: Devolucion Exitosa\n")
        f.write("==========================================\n")

    print("\n  Devolucion registrada con exito!")
    print("  Certificado TXT generado: " + ruta_txt)

    # Generar certificado PDF
    ruta_pdf = os.path.join("certificados", nombre_base + ".pdf")
    generar_pdf_certificado(prestamo_elegido, dias, ruta_pdf)

    # Guardar en CSV
    guardar_devolucion_en_csv(prestamo_elegido, dias)


# ------------------------------------------------------------------
# Opcion 4: Items con mas de 30 dias (ventas automaticas)
# ------------------------------------------------------------------

def consultar_y_procesar_morosos(prestamos, items, ventas):
    print("\n--- Items con mas de 30 dias de prestamo ---")

    # Buscar todos los prestamos activos que ya superaron los 30 dias
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

    for p in morosos:
        dias     = calcular_dias_transcurridos(p["fecha_inicio"])
        subtotal = p["item_precio"]
        impuesto = subtotal * IMPUESTO_CONCHUDEZ
        total    = subtotal + impuesto

        print("  Usuario : " + p["usuario_nombre"])
        print("  Item    : " + p["item_nombre"] + " (ID: " + p["item_id"] + ")")
        print("  Dias    : " + str(dias) + " dias")
        print("  Subtotal: $" + "{:,.2f}".format(subtotal))
        print("  Impuesto conchudez 23%: $" + "{:,.2f}".format(impuesto))
        print("  TOTAL   : $" + "{:,.2f}".format(total))
        print("  " + "-" * 40)

        # Crear el registro de la venta
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

        # El item queda como vendido (no vuelve al inventario)
        for item in items:
            if item["id"] == p["item_id"]:
                item["disponible"] = False
                break

        nombre_base = p["usuario_nombre"].replace(" ", "_") + "_" + p["item_id"]

        # Generar factura TXT
        ruta_txt = os.path.join("facturas", nombre_base + "_FACTURA.txt")

        with open(ruta_txt, "w", encoding="utf-8") as f:
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

        print("  Factura TXT generada: " + ruta_txt)

        # Generar factura PDF
        ruta_pdf = os.path.join("facturas", nombre_base + "_FACTURA.pdf")
        generar_pdf_factura(nueva_venta, ruta_pdf)

        # Guardar en CSV
        guardar_venta_en_csv(nueva_venta)

    print("\n  Se procesaron " + str(len(morosos)) + " venta(s) por mora.")


# ------------------------------------------------------------------
# Opcion 5: Consultar articulos prestados
# ------------------------------------------------------------------

def consultar_estado_general(prestamos):
    print("\n--- Consultar Articulos Prestados ---")

    # Filtrar solo los prestamos que estan activos
    activos = []
    for p in prestamos:
        if p["activo"] == True:
            activos.append(p)

    if len(activos) == 0:
        print("  No hay prestamos activos para mostrar.")
        return

    # Calcular los dias de cada prestamo activo
    reporte = []
    for p in activos:
        dias = calcular_dias_transcurridos(p["fecha_inicio"])
        reporte.append({
            "id":      p["item_id"],
            "item":    p["item_nombre"],
            "usuario": p["usuario_nombre"],
            "dias":    dias
        })

    # Ordenar de mayor a menor por dias (algoritmo burbuja)
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
            r["id"], r["item"][:20], str(r["dias"]), r["usuario"][:20]
        ))

    print("  " + "-" * 60)

    # Guardar el reporte en un archivo de texto
    ruta_reporte  = os.path.join("reportes", "estado_prestamos.txt")
    fecha_reporte = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(ruta_reporte, "w", encoding="utf-8") as f:
        f.write("REPORTE DE ESTADO GENERAL - " + fecha_reporte + "\n")
        f.write("-" * 60 + "\n")
        f.write("{:<12} {:<22} {:<6} {}\n".format("ID", "Item", "Dias", "Usuario"))
        f.write("-" * 60 + "\n")
        for r in reporte:
            f.write("{:<12} {:<22} {:<6} {}\n".format(
                r["id"], r["item"][:20], str(r["dias"]), r["usuario"][:20]
            ))

    print("\n  Reporte guardado en: " + ruta_reporte)