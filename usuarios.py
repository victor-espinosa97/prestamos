import re

def validar_nombre(nombre):
    return nombre.isalpha() and len(nombre) >= 3

def validar_documento(doc):
    return doc.isdigit() and 3 <= len(doc) <= 15

def validar_correo(correo):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.com$', correo)

def validar_tiempo(tiempo):
    return tiempo in [5, 10, 15, 30]

# Esta es una funcion para registrar un usuario
def registrar_usuario(usuarios): 
    # 
    nombre = input("Nombre: ")

    if not validar_nombre(nombre):
        print("Nombre inválido")
        return

    apellido = input("Apellido: ")
    if not validar_nombre(apellido):
        print("Apellido inválido")
        return

    doc = input("Documento: ")
    if not validar_documento(doc):
        print("Documento inválido")
        return

    correo = input("Correo: ")
    if not validar_correo(correo):
        print("Correo inválido")
        return

    tiempo = int(input("Tiempo (5,10,15,30): "))
    if not validar_tiempo(tiempo):
        print("Tiempo inválido")
        return

    usuarios.append({
        "doc": doc,
        "nombre": nombre,
        "apellido": apellido,
        "correo": correo,
        "tiempo": tiempo,
        "prestamos": 0
    })

    print("Usuario registrado ✔")