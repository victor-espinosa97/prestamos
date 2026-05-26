import os
from datetime import datetime

IMPUESTO_CONCHUDEZ = 0.23


# ------------------------------------------------------------------
# Función auxiliar
# ------------------------------------------------------------------

def calcular_dias_transcurridos(fecha_inicio_str):
    """Calcula cuántos días han pasado desde la fecha de inicio del préstamo."""
    fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d %H:%M:%S")
    diferencia = datetime.now() - fecha_inicio
    return diferencia.days


# ------------------------------------------------------------------
# Registrar préstamo
# ------------------------------------------------------------------

def registrar_prestamo(usuarios, items, prestamos):
    """
    Registra un préstamo nuevo.
    - Verifica que el usuario exista.
    - Muestra el inventario disponible y permite elegir por ID.
    - Guarda de inmediato al finalizar.
    """
    print("\n--- Registrar Nuevo Prestamo ---")

    # --- Buscar usuario por documento ---
    doc = ""
    usuario = None
    while True:
        doc = input("Documento del usuario: ").strip()

        # Buscar en la lista de usuarios
        for u in usuarios:
            if u["doc"] == doc:
                usuario = u
                break

        if usuario is not None:
            print("  Usuario encontrado: " + usuario["nombre"] + " " + usuario["apellido"])
            break
        else:
            print("  ERROR: No existe un usuario con ese documento.")
            print("  MJ debe registrar al usuario antes de hacer un prestamo.")
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
    print("  " + "-" * 45)
    print("  {:<12} {:<20} {:<12}".format("ID", "Nombre", "Categoria"))
    print("  " + "-" * 45)
    for item in disponibles:
        print("  {:<12} {:<20} {:<12}".format(item["id"], item["nombre"][:20], item["categoria"]))
    print("  " + "-" * 45)

    # --- Seleccionar ítem por ID ---
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

    # --- Registrar el préstamo ---
    fecha_ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    nuevo_prestamo = {
        "usuario_doc":    doc,
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

    print("\n  Prestamo registrado con exito para " + usuario["nombre"] + "!")
    print("  Item       : " + item_seleccionado["nombre"])
    print("  Dias pactados: " + str(usuario["tiempo"]) + " dias")
    print("  Fecha inicio : " + fecha_ahora)


# ------------------------------------------------------------------
# Registrar devolución
# ------------------------------------------------------------------

def registrar_devolucion(prestamos, items):
    """
    Registra la devolución de un préstamo activo.
    - Verifica que el usuario tenga préstamos activos.
    - Si se devuelve antes de los 30 días, genera certificado TXT.
    - Guarda de inmediato al finalizar.
    """
    print("\n--- Registrar Devolucion ---")

    doc = input("Documento del usuario: ").strip()

    # Buscar préstamos activos del usuario
    prestamos_activos = []
    for p in prestamos:
        if p["usuario_doc"] == doc and p["activo"] == True:
            prestamos_activos.append(p)

    if len(prestamos_activos) == 0:
        print("  El usuario no tiene prestamos activos. No se puede registrar devolucion.")
        return

    # Mostrar sus préstamos activos
    print("\n  Prestamos activos del usuario:")
    for i in range(len(prestamos_activos)):
        p = prestamos_activos[i]
        dias_transcurridos = calcular_dias_transcurridos(p["fecha_inicio"])
        print("  " + str(i + 1) + ". " + p["item_nombre"] + " (ID: " + p["item_id"] + ") - " + str(dias_transcurridos) + " dias transcurridos")

    # Seleccionar cuál devolver
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

    # Verificar si superó los 30 días
    dias = calcular_dias_transcurridos(prestamo_elegido["fecha_inicio"])

    if dias > 30:
        print("\n  AVISO: Este prestamo supero los 30 dias.")
        print("  Debe procesarse como VENTA en el panel de administracion.")
        return

    # Procesar devolución
    prestamo_elegido["activo"] = False

    # Devolver el ítem al inventario
    for item in items:
        if item["id"] == prestamo_elegido["item_id"]:
            item["disponible"] = True
            break

    # Generar certificado TXT
    fecha_dev = datetime.now().strftime("%Y-%m-%d")
    fecha_dev_completa = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Nombre del archivo: NombreUsuario_FechaDevolucion_IDItem.txt
    nombre_archivo = prestamo_elegido["usuario_nombre"].replace(" ", "_")
    nombre_archivo = nombre_archivo + "_" + fecha_dev + "_" + prestamo_elegido["item_id"] + ".txt"
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
# Procesar ventas automáticas (préstamos > 30 días)
# ------------------------------------------------------------------

def procesar_ventas_automaticas(prestamos, items, ventas):
    """
    Revisa todos los préstamos activos.
    Si alguno supera los 30 días, lo convierte en venta automáticamente
    y genera la factura en un archivo TXT.
    """
    contador = 0

    for p in prestamos:
        if p["activo"] == True:
            dias = calcular_dias_transcurridos(p["fecha_inicio"])

            if dias > 30:
                # Calcular valores de la venta
                subtotal = p["item_precio"]
                impuesto = subtotal * IMPUESTO_CONCHUDEZ
                total    = subtotal + impuesto

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

                # Cerrar el préstamo
                p["activo"] = False

                # El ítem queda marcado como no disponible (fue vendido)
                for item in items:
                    if item["id"] == p["item_id"]:
                        item["disponible"] = False
                        break

                # Generar factura TXT
                nombre_factura = p["usuario_nombre"].replace(" ", "_") + "_" + p["item_id"] + "_FACTURA.txt"
                ruta_factura = os.path.join("facturas", nombre_factura)

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

                contador = contador + 1

    if contador > 0:
        print("  Se procesaron " + str(contador) + " ventas automaticas por mora.")


# ------------------------------------------------------------------
# Consultar estado general de préstamos
# ------------------------------------------------------------------

def consultar_estado_general(prestamos):
    """
    Muestra todos los préstamos activos ordenados por cantidad de días
    (de mayor a menor) y guarda el reporte en un archivo plano.
    """
    print("\n--- Estado General de Prestamos ---")

    # Filtrar solo los activos
    activos = []
    for p in prestamos:
        if p["activo"] == True:
            activos.append(p)

    if len(activos) == 0:
        print("  No hay prestamos activos para reportar.")
        return

    # Calcular días de cada préstamo y armar lista de reporte
    reporte = []
    for p in activos:
        dias = calcular_dias_transcurridos(p["fecha_inicio"])
        reporte.append({
            "item":    p["item_nombre"],
            "usuario": p["usuario_nombre"],
            "dias":    dias,
            "id":      p["item_id"]
        })

    # Ordenar de mayor a menor días (ordenamiento burbuja básico)
    for i in range(len(reporte)):
        for j in range(i + 1, len(reporte)):
            if reporte[j]["dias"] > reporte[i]["dias"]:
                temp      = reporte[i]
                reporte[i] = reporte[j]
                reporte[j] = temp

    # Mostrar en pantalla y guardar en archivo
    os.makedirs("reportes", exist_ok=True)
    ruta_reporte = os.path.join("reportes", "estado_prestamos.txt")
    fecha_reporte = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    encabezado = "\n  {:<12} {:<22} {:<6} {}".format("ID", "Item", "Dias", "Usuario")
    separador  = "  " + "-" * 60

    print(encabezado)
    print(separador)

    with open(ruta_reporte, "w", encoding="utf-8") as f:
        f.write("REPORTE DE ESTADO GENERAL - " + fecha_reporte + "\n")
        f.write("-" * 60 + "\n")
        f.write("{:<12} {:<22} {:<6} {}\n".format("ID", "Item", "Dias", "Usuario"))
        f.write("-" * 60 + "\n")

        for r in reporte:
            linea = "  {:<12} {:<22} {:<6} {}".format(
                r["id"], r["item"][:20], str(r["dias"]), r["usuario"][:20]
            )
            linea_archivo = "{:<12} {:<22} {:<6} {}\n".format(
                r["id"], r["item"][:20], str(r["dias"]), r["usuario"][:20]
            )
            print(linea)
            f.write(linea_archivo)

    print(separador)
    print("\n  Reporte guardado en: " + ruta_reporte)