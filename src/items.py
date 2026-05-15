import random
import string

CATEGORIAS = {
    "1": ("Videojuegos", "VID"),
    "2": ("Libros", "LIB"),
    "3": ("Música y video", "MUS"),
    "4": ("Herramientas", "HER"),
    "5": ("Dinero", "DIN"),
    "6": ("Misceláneo y varios", "MIS")
}

def calcular_estado_difuso(funcionalidad, estetica):
    """
    Aplica lógica difusa simple mediante un promedio ponderado
    para determinar la calidad del ítem.
    """
    puntaje = (funcionalidad * 0.7) + (estetica * 0.3)
    
    if puntaje >= 9: return "Excelente (Como nuevo)"
    if puntaje >= 7: return "Bueno (Desgaste mínimo)"
    if puntaje >= 5: return "Regular (Funcional con detalles)"
    return "Malo (Requiere mantenimiento o reposición)"

def generar_id(prefijo):
    # Prefijo de categoría + 4 caracteres alfanuméricos únicos
    aleatorio = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{prefijo}-{aleatorio}"

def registrar_item(items):
    print("\n--- Registro de Ítem ---")
    nombre = input("Nombre del ítem: ")
    if len(nombre) < 3:
        print("Error: El nombre es muy corto.")
        return

    print("Seleccione Categoría:")
    for k, v in CATEGORIAS.items():
        print(f"{k}. {v[0]}")
    
    opcion = input("Opción: ")
    if opcion not in CATEGORIAS:
        print("Error: Categoría no válida.")
        return
    
    cat_nombre, cat_prefijo = CATEGORIAS[opcion]

    try:
        precio = float(input("Precio de compra: "))
        print("\nValoración de estado (Escala 1-10):")
        f = int(input("Calidad de funcionamiento: "))
        e = int(input("Estado estético/físico: "))
        if not (1 <= f <= 10 and 1 <= e <= 10):
            raise ValueError
    except ValueError:
        print("Error: Ingrese valores numéricos válidos.")
        return

    estado_final = calcular_estado_difuso(f, e)

    nuevo_item = {
        "id": generar_id(cat_prefijo),
        "nombre": nombre,
        "categoria": cat_nombre,
        "precio": precio,
        "estado": estado_final,
        "disponible": True
    }

    items.append(nuevo_item)
    print(f"Item registrado con ID: {nuevo_item['id']} | Estado: {estado_final} ✔")