import json
import os

def cargar_datos(ruta):
    """Lee un archivo JSON y retorna su contenido como lista."""
    if not os.path.exists(ruta):
        return []
    if os.path.getsize(ruta) == 0:
        return []
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def guardar_datos(ruta, datos):
    """Guarda una lista en un archivo JSON."""
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)