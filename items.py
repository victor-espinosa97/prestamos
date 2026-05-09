import random
import string

categorias = {
    "Videojuegos": "VID",
    "Libros": "LIB",
    "Musica": "MUS",
    "Herramientas": "HER",
    "Dinero": "DIN",
    "Miscelaneo": "MIS"
}

def generar_id(categoria):
    return categorias[categoria] + ''.join(random.choices(string.digits, k=4))

def registrar_item(items):
    nombre = input("Nombre: ")
    if len(nombre) < 3:
        print("Nombre inválido")
        return

    print("Categorías:", list(categorias.keys()))
    categoria = input("Categoría: ")

    if categoria not in categorias:
        print("Categoría inválida")
        return

    precio = float(input("Precio: "))
    estado = input("Estado (malo, regular, bueno): ")

    items.append({
        "id": generar_id(categoria),
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "estado": estado,
        "disponible": True
    })

    print("Item registrado ✔")