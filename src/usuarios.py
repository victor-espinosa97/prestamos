# ============================================================
# MODULO: usuarios.py
# DESCRIPCION: Registro y validacion de usuarios del sistema
# ============================================================


# ------------------------------------------------------------------
# Funciones de validacion
# ------------------------------------------------------------------

def validar_nombre_apellido(texto):
    """
    Valida que el texto tenga al menos 3 caracteres y no contenga numeros.
    Retorna True si es valido, False si no.
    """
    # Condicion 1: longitud minima de 3
    if len(texto) < 3:
        return False

    # Condicion 2: no puede tener numeros
    for caracter in texto:
        if caracter.isdigit():
            return False

    return True


def validar_documento(doc):
    """
    Valida que el documento tenga entre 3 y 15 digitos y sea solo numeros.
    """
    # Condicion 1: solo numeros
    if not doc.isdigit():
        return False

    # Condicion 2: longitud entre 3 y 15
    if len(doc) < 3 or len(doc) > 15:
        return False

    return True


def validar_correo(correo):
    """
    Que tenga el correo
    """
    # Condición 1: debe tener exactamente una arroba
    if correo.endswith('@udea.edu.co'):
        return True

    return False


# ------------------------------------------------------------------
# Funcion principal de registro
# ------------------------------------------------------------------

def registrar_usuario(usuarios):
    """
    Registra un nuevo usuario en el sistema.
    Cada campo tiene su propio bucle: si el dato es incorrecto,
    el programa muestra el error y vuelve a pedir ESE MISMO campo.
    """
    print("\n--- Registro de Nuevo Usuario ---")

    # --- Campo: Nombre ---
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

    # --- Campo: Apellido ---
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

    # --- Campo: Documento ---
    doc = ""
    while True:
        doc = input("Numero de documento (solo numeros, 3-15 digitos): ").strip()

        if not validar_documento(doc):
            if not doc.isdigit():
                print("  ERROR: El documento solo puede contener numeros. Intente de nuevo.")
            else:
                print("  ERROR: El documento debe tener entre 3 y 15 digitos. Intente de nuevo.")
            continue

        # Verificar que el documento no este duplicado
        ya_existe = False
        for u in usuarios:
            if u["doc"] == doc:
                ya_existe = True
                break

        if ya_existe:
            print("  ERROR: Ya existe un usuario con ese documento. Intente con otro.")
        else:
            break

    # --- Campo: Correo ---
    correo = ""
    while True:
        correo = input("Correo electronico (ej: nombre@gmail.com): ").strip()
        if validar_correo(correo):
            break
        else:
            print("  ERROR: Correo invalido. Debe tener '@' y terminar en '.com'. Intente de nuevo.")

    # --- Campo: Tiempo de prestamo ---
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

    # --- Guardar usuario ---
    nuevo_usuario = {
        "doc":                  doc,
        "nombre":               nombre,
        "apellido":             apellido,
        "correo":               correo,
        "tiempo":               tiempo,
        "prestamos_realizados": 0
    }

    usuarios.append(nuevo_usuario)

    print("\n  Usuario '" + nombre + " " + apellido + "' registrado con exito!")