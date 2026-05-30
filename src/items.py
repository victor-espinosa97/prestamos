# items.py
# Registro de items (objetos a prestar) en el inventario

import random
import string
import csv
import os
from datetime import datetime

# Categorias disponibles para clasificar los items
# Clave: numero que escoge el usuario
# Valor: (nombre de la categoria, prefijo para el ID)
CATEGORIAS = {
    "1": ("Videojuegos",    "VID"),
    "2": ("Libros",         "LIB"),
    "3": ("Musica y video", "MUS"),
    "4": ("Herramientas",   "HER"),
    "5": ("Dinero",         "DIN"),
    "6": ("Miscelaneo",     "MIS")
}


def calcular_estado_difuso(funcionalidad, estetica):
    # Logica difusa: combina funcionamiento (70%) y apariencia (30%)
    # para determinar el estado general del item
    puntaje = (funcionalidad * 0.7) + (estetica * 0.3)

    if puntaje >= 9:
        return "Excelente (Como nuevo)"
    elif puntaje >= 7:
        return "Bueno (Desgaste minimo)"
    elif puntaje >= 5:
        return "Regular (Funcional con detalles)"
    else:
        return "Malo (Requiere mantenimiento)"


def generar_id(prefijo):
    # Genera un ID unico con el prefijo de la categoria + 4 caracteres aleatorios
    # Ejemplos: VID-A3K9, LIB-X7B2, HER-QP12
    caracteres = string.ascii_uppercase + string.digits
    aleatorio  = ""
    for _ in range(4):
        aleatorio = aleatorio + random.choice(caracteres)
    return prefijo + "-" + aleatorio


def guardar_item_en_csv(item):
    # Guarda los datos del item en data/items.csv
    # Si el archivo no existe lo crea con encabezados
    # Si ya existe agrega una fila al final sin borrar lo anterior
    ruta           = os.path.join("data", "items.csv")
    archivo_existe = os.path.exists(ruta)

    with open(ruta, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)

        if not archivo_existe:
            escritor.writerow(["fecha", "id", "nombre", "categoria", "precio", "estado"])

        escritor.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            item["id"],
            item["nombre"],
            item["categoria"],
            "{:.2f}".format(item["precio"]),
            item["estado"]
        ])

    print("  Item guardado en data/items.csv")


def registrar_item(items):
    print("\n--- Registro de Nuevo Item ---")

    # Campo: Nombre del item
    nombre = ""
    while True:
        nombre = input("Nombre del item: ").strip()
        if len(nombre) >= 3:
            break
        else:
            print("  ERROR: El nombre debe tener al menos 3 caracteres. Intente de nuevo.")

    # Campo: Categoria
    cat_nombre  = ""
    cat_prefijo = ""
    while True:
        print("\n  Categorias disponibles:")
        for k, v in CATEGORIAS.items():
            print("    " + k + ". " + v[0])
        opcion = input("  Seleccione una opcion (1-6): ").strip()

        if opcion in CATEGORIAS:
            cat_nombre  = CATEGORIAS[opcion][0]
            cat_prefijo = CATEGORIAS[opcion][1]
            break
        else:
            print("  ERROR: Opcion no valida. Debe elegir un numero del 1 al 6.")

    # Campo: Precio de compra
    precio = 0.0
    while True:
        entrada = input("Precio de compra (solo numeros, ej: 25000): ").strip()

        # Verificar manualmente que sea un numero valido
        es_numero = True
        puntos    = 0
        for caracter in entrada:
            if caracter == ".":
                puntos = puntos + 1
            elif not caracter.isdigit():
                es_numero = False
                break

        if not es_numero or puntos > 1 or len(entrada) == 0:
            print("  ERROR: Ingrese un valor numerico valido (ej: 25000 o 25000.50).")
            continue

        precio = float(entrada)

        if precio <= 0:
            print("  ERROR: El precio debe ser mayor a cero.")
        else:
            break

    # Campo: Estado del item con logica difusa
    print("\n  Valoracion del estado del item (escala del 1 al 10):")

    funcionalidad = 0
    while True:
        entrada = input("  Calidad de funcionamiento (1-10): ").strip()
        if not entrada.isdigit():
            print("  ERROR: Ingrese un numero entero del 1 al 10.")
            continue
        funcionalidad = int(entrada)
        if funcionalidad >= 1 and funcionalidad <= 10:
            break
        else:
            print("  ERROR: El valor debe estar entre 1 y 10.")

    estetica = 0
    while True:
        entrada = input("  Estado estetico/fisico (1-10): ").strip()
        if not entrada.isdigit():
            print("  ERROR: Ingrese un numero entero del 1 al 10.")
            continue
        estetica = int(entrada)
        if estetica >= 1 and estetica <= 10:
            break
        else:
            print("  ERROR: El valor debe estar entre 1 y 10.")

    estado_final = calcular_estado_difuso(funcionalidad, estetica)

    # Guardar en memoria
    nuevo_item = {
        "id":         generar_id(cat_prefijo),
        "nombre":     nombre,
        "categoria":  cat_nombre,
        "precio":     precio,
        "estado":     estado_final,
        "disponible": True
    }

    items.append(nuevo_item)

    # Guardar en CSV
    guardar_item_en_csv(nuevo_item)

    print("\n  Item registrado con exito!")
    print("  ID asignado : " + nuevo_item["id"])
    print("  Categoria   : " + cat_nombre)
    print("  Estado      : " + estado_final)