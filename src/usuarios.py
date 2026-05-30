# usuarios.py
# Registro y validacion de usuarios del sistema

import csv
import os
from datetime import datetime


# ------------------------------------------------------------------
# Funciones de validacion
# ------------------------------------------------------------------

def validar_nombre_apellido(texto):
    # Verifica que el texto tenga al menos 3 letras y no tenga numeros
    if len(texto) < 3:
        return False
    for caracter in texto:
        if caracter.isdigit():
            return False
    return True


def validar_documento(doc):
    # Verifica que el documento sea solo numeros y tenga entre 3 y 15 digitos
    if not doc.isdigit():
        return False
    if len(doc) < 3 or len(doc) > 15:
        return False
    return True


def validar_correo(correo):
    # Verifica que el correo tenga una @ y termine en .com
    # Ejemplos validos: juan@gmail.com, maria@hotmail.com
    if correo.count("@") != 1:
        return False
    partes        = correo.split("@")
    parte_antes   = partes[0]
    parte_despues = partes[1]
    if len(parte_antes) == 0:
        return False
    if not parte_despues.endswith(".com"):
        return False
    if parte_despues == ".com":
        return False
    return True


# ------------------------------------------------------------------
# Guardar en CSV
# ------------------------------------------------------------------

def guardar_usuario_en_csv(usuario):
    # Guarda los datos del usuario en data/usuarios.csv
    # Si el archivo no existe lo crea con encabezados
    # Si ya existe agrega una fila al final sin borrar lo anterior
    ruta           = os.path.join("data", "usuarios.csv")
    archivo_existe = os.path.exists(ruta)

    with open(ruta, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)

        if not archivo_existe:
            escritor.writerow(["fecha", "documento", "nombre", "apellido", "correo", "dias_prestamo"])

        escritor.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            usuario["doc"],
            usuario["nombre"],
            usuario["apellido"],
            usuario["correo"],
            str(usuario["tiempo"])
        ])

    print("  Usuario guardado en data/usuarios.csv")


# ------------------------------------------------------------------
# Registro de usuario
# ------------------------------------------------------------------

def registrar_usuario(usuarios):
    print("\n--- Registro de Nuevo Usuario ---")

    # Campo: Documento
    doc = ""
    while True:
        doc = input("Numero de documento (solo numeros, 3-15 digitos): ").strip()

        if not validar_documento(doc):
            if not doc.isdigit():
                print("  ERROR: El documento solo puede contener numeros. Intente de nuevo.")
            else:
                print("  ERROR: El documento debe tener entre 3 y 15 digitos. Intente de nuevo.")
            continue

        # Verificar que el documento no este ya registrado
        ya_existe = False
        for u in usuarios:
            if u["doc"] == doc:
                ya_existe = True
                break

        if ya_existe:
            print("  ERROR: Ya existe un usuario con ese documento. Intente con otro.")
        else:
            break

    # Campo: Nombre
    nombre = ""
    while True:
        nombre = input("Nombre: ").strip()
        if validar_nombre_apellido(nombre):
            break
        else:
            if len(nombre) < 3:
                print("  ERROR: El nombre debe tener al menos 3 letras. Intente de nuevo.")
            else:
                print("  ERROR: El nombre no puede contener numeros. Intente de nuevo.")

    # Campo: Apellido
    apellido = ""
    while True:
        apellido = input("Apellido: ").strip()
        if validar_nombre_apellido(apellido):
            break
        else:
            if len(apellido) < 3:
                print("  ERROR: El apellido debe tener al menos 3 letras. Intente de nuevo.")
            else:
                print("  ERROR: El apellido no puede contener numeros. Intente de nuevo.")

    # Campo: Correo
    correo = ""
    while True:
        correo = input("Correo electronico (ej: nombre@gmail.com): ").strip()
        if validar_correo(correo):
            break
        else:
            print("  ERROR: Correo invalido. Debe tener '@' y terminar en '.com'. Intente de nuevo.")

    # Campo: Tiempo de prestamo
    tiempo = 0
    while True:
        print("  Opciones de tiempo: 5, 10, 15 o 30 dias")
        entrada = input("  Seleccione el tiempo de prestamo: ").strip()

        if not entrada.isdigit():
            print("  ERROR: Debe ingresar un numero. Intente de nuevo.")
            continue

        tiempo = int(entrada)

        if tiempo == 5 or tiempo == 10 or tiempo == 15 or tiempo == 30:
            break
        else:
            print("  ERROR: Tiempo no permitido. Solo se aceptan 5, 10, 15 o 30 dias.")

    # Guardar en memoria
    nuevo_usuario = {
        "doc":                  doc,
        "nombre":               nombre,
        "apellido":             apellido,
        "correo":               correo,
        "tiempo":               tiempo,
        "prestamos_realizados": 0
    }

    usuarios.append(nuevo_usuario)

    # Guardar en CSV
    guardar_usuario_en_csv(nuevo_usuario)

    print("\n  Usuario '" + nombre + " " + apellido + "' registrado con exito!")