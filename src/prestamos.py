from datetime import datetime
import os

# Constante de impuesto solicitada
IMPUESTO_CONCHUDEZ = 0.23

def calcular_dias_transcurridos(fecha_inicio_str):
    fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d %H:%M:%S")
    diferencia = datetime.now() - fecha_inicio
    return diferencia.days

def registrar_prestamo(usuarios, items, prestamos):
    print("\n--- Nuevo Préstamo ---")
    doc = input("Documento del usuario: ")
    
    usuario = next((u for u in usuarios if u["doc"] == doc), None)
    if not usuario:
        print("Usuario no existe ❌. MJ, debe registrar al usuario nuevo.")
        return

    print("\nInventario Disponible:")
    disponibles = [i for i in items if i["disponible"]]
    if not disponibles:
        print("No hay ítems disponibles en este momento.")
        return

    for i in disponibles:
        print(f"[{i['id']}] {i['nombre']} - Cat: {i['categoria']}")

    item_id = input("\nIngrese el ID del ítem a prestar: ")
    item = next((i for i in disponibles if i["id"] == item_id), None)

    if not item:
        print("ID de ítem no válido o no disponible ❌")
        return

    # Registrar el préstamo
    fecha_ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nuevo_p = {
        "usuario_doc": doc,
        "usuario_nombre": f"{usuario['nombre']} {usuario['apellido']}",
        "item_id": item_id,
        "item_nombre": item["nombre"],
        "item_precio": item["precio"],
        "fecha_inicio": fecha_ahora,
        "dias_pactados": usuario["tiempo"],
        "activo": True
    }
    
    prestamos.append(nuevo_p)
    item["disponible"] = False
    usuario["prestamos_realizados"] += 1
    print(f"Préstamo registrado con éxito para {usuario['nombre']} ✔")

def registrar_devolucion(prestamos, items):
    print("\n--- Registrar Devolución ---")
    doc = input("Documento del usuario: ")
    
    # Buscar préstamos activos de ese usuario
    prestamos_activos = [p for p in prestamos if p["usuario_doc"] == doc and p["activo"]]
    
    if not prestamos_activos:
        print("El usuario no tiene préstamos activos ❌")
        return

    print("Préstamos actuales:")
    for idx, p in enumerate(prestamos_activos):
        print(f"{idx + 1}. Item: {p['item_nombre']} (ID: {p['item_id']})")
    
    try:
        sel = int(input("Seleccione el número del préstamo a devolver: ")) - 1
        prestamo = prestamos_activos[sel]
    except (ValueError, IndexError):
        print("Selección inválida.")
        return

    # Validar si es devolución o si ya pasó a venta (más de 30 días)
    dias = calcular_dias_transcurridos(prestamo["fecha_inicio"])
    
    if dias > 30:
        print("⚠️ Este préstamo superó los 30 días. Debe procesarse como VENTA en el módulo administrativo.")
        return

    # Procesar devolución
    prestamo["activo"] = False
    item = next(i for i in items if i["id"] == prestamo["item_id"])
    item["disponible"] = True
    
    # Generar Certificado TXT
    fecha_dev = datetime.now().strftime("%Y-%m-%d")
    nombre_archivo = f"certificados/{prestamo['usuario_nombre'].replace(' ', '_')}_{fecha_dev}_{prestamo['item_id']}.txt"
    
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("==========================================\n")
        f.write("       CERTIFICADO DE DEVOLUCIÓN         \n")
        f.write("==========================================\n")
        f.write(f"Usuario: {prestamo['usuario_nombre']}\n")
        f.write(f"Ítem: {prestamo['item_nombre']} (ID: {prestamo['item_id']})\n")
        f.write(f"Fecha Préstamo: {prestamo['fecha_inicio']}\n")
        f.write(f"Fecha Devolución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("==========================================\n")
        f.write("Estado: Devolución Exitosa\n")

    print(f"Devolución registrada. Certificado generado: {nombre_archivo} ✔")

def procesar_ventas_automaticas(prestamos, items, ventas):
    """
    Escanea préstamos activos. Si superan los 30 días, los convierte en venta.
    """
    count = 0
    for p in prestamos:
        if p["activo"]:
            dias = calcular_dias_transcurridos(p["fecha_inicio"])
            if dias > 30:
                # Calcular valores
                subtotal = p["item_precio"]
                impuesto = subtotal * IMPUESTO_CONCHUDEZ
                total = subtotal + impuesto
                
                # Crear factura
                venta = {
                    "usuario": p["usuario_nombre"],
                    "item_id": p["item_id"],
                    "item_nombre": p["item_nombre"],
                    "subtotal": subtotal,
                    "impuesto": impuesto,
                    "total": total,
                    "motivo": "Excedió el tiempo máximo de préstamo (30 días)"
                }
                ventas.append(venta)
                
                # Desactivar préstamo y el ítem queda 'vendido' (no disponible)
                p["activo"] = False
                item = next(i for i in items if i["id"] == p["item_id"])
                item["disponible"] = False # No vuelve al inventario porque se vendió
                
                # Generar Factura TXT
                nombre_factura = f"{p['usuario_nombre'].replace(' ', '_')}_{p['item_id']}_FACTURA.txt"
                with open(nombre_factura, "w", encoding="utf-8") as f:
                    f.write("==========================================\n")
                    f.write("           FACTURA DE VENTA              \n")
                    f.write("==========================================\n")
                    f.write(f"Cliente: {venta['usuario']}\n")
                    f.write(f"Producto: {venta['item_nombre']} (ID: {venta['item_id']})\n")
                    f.write(f"Motivo: {venta['motivo']}\n")
                    f.write("------------------------------------------\n")
                    f.write(f"Subtotal: ${subtotal:,.2f}\n")
                    f.write(f"Impuesto Conchudez (23%): ${impuesto:,.2f}\n")
                    f.write(f"TOTAL A PAGAR: ${total:,.2f}\n")
                    f.write("==========================================\n")
                
                count += 1
    
    if count > 0:
        print(f"Se han procesado {count} ventas automáticas por mora. ✔")


# Informe general
def consultar_estado_general(prestamos):
    print("\n--- Estado General de Préstamos (Ordenado por Antigüedad) ---")
    
    activos = [p for p in prestamos if p["activo"]]
    
    if not activos:
        print("No hay préstamos activos para reportar.")
        return

    # Calculamos los días para cada préstamo
    reporte_datos = []
    for p in activos:
        dias = calcular_dias_transcurridos(p["fecha_inicio"])
        reporte_datos.append({
            "item": p["item_nombre"],
            "usuario": p["usuario_nombre"],
            "dias": dias,
            "id": p["item_id"]
        })

    # Ordenar por cantidad de días (de mayor a menor)
    reporte_datos.sort(key=lambda x: x["dias"], reverse=True)

    # SOLUCIÓN: Definir rutas de forma segura y garantizar que el directorio exista
    ruta_directorio = "reportes"
    ruta_archivo = os.path.join(ruta_directorio, "estadisticas_prestamos.txt")
    
    # Crea la carpeta data si por algún motivo no existe en este punto de la ejecución
    os.makedirs(ruta_directorio, exist_ok=True)

    # Mostrar en pantalla y guardar en archivo plano estadisticas.txt
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(f"REPORTE DE ESTADO GENERAL - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-" * 50 + "\n")
        
        header = f"{'Ítem':<20} | {'Días':<5} | {'Usuario':<20}"
        print(header)
        f.write(header + "\n")
        
        for r in reporte_datos:
            linea = f"{r['item'][:20]:<20} | {r['dias']:<5} | {r['usuario'][:20]:<20}"
            print(linea)
            f.write(linea + "\n")
            
    print(f"\nReporte generado y guardado en: {ruta_archivo} ✔")