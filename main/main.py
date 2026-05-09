from usuarios import registrar_usuario
from items import registrar_item
from prestamos import registrar_prestamo, devolver
from archivos import cargar_datos, guardar_datos

# rutas
ruta_usuarios = "data/usuarios.json"
ruta_items = "data/items.json"
ruta_prestamos = "data/prestamos.json"

# cargar datos
usuarios = cargar_datos(ruta_usuarios)
items = cargar_datos(ruta_items)
prestamos = cargar_datos(ruta_prestamos)

while True:
    print("\n--- SISTEMA ---")
    print("1. Registrar usuario")
    print("2. Registrar item")
    print("3. Préstamo")
    print("4. Devolución")
    print("5. Salir")

    op = input("Opción: ")

    if op == "1":
        registrar_usuario(usuarios)
        guardar_datos(ruta_usuarios, usuarios)

    elif op == "2":
        registrar_item(items)
        guardar_datos(ruta_items, items)

    elif op == "3":
        registrar_prestamo(usuarios, items, prestamos)
        guardar_datos(ruta_prestamos, prestamos)
        guardar_datos(ruta_items, items)

    elif op == "4":
        devolver(prestamos, items)
        guardar_datos(ruta_prestamos, prestamos)
        guardar_datos(ruta_items, items)

    elif op == "5":
        break