import json
import os

def cargar_datos(ruta):
    if not os.path.exists(ruta):
        return []

    if os.path.getsize(ruta) == 0:
        return []

    try:
        with open(ruta, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def guardar_datos(ruta, datos):
    with open(ruta, "w") as f:
        json.dump(datos, f, indent=4)