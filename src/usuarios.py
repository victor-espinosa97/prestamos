import archivos

DATA_USUARIOS = "data/usuarios.json"

# ------------------------------------------------------------------
# Funciones de validación (sin expresiones regulares)
# ------------------------------------------------------------------

def validar_nombre_apellido(texto):
    """
    Valida que el texto tenga al menos 3 caracteres y no contenga números.
    Retorna True si es válido, False si no.
    """
    # Condición 1: longitud mínima de 3
    if len(texto) < 3:
        return False

    # Condición 2: no puede tener números
    # Recorremos cada caracter y si alguno es dígito(numero), no es válido
    for caracter in texto:
        if caracter.isdigit():
            return False

    return True


def validar_documento(doc):
    """
    Valida que el documento tenga entre 3 y 15 dígitos y sea solo números.
    """
    # Condición 1: solo números
    if not doc.isdigit():
        return False

    # Condición 2: longitud entre 3 y 15
    if len(doc) < 3 or len(doc) > 15:
        return False

    return True


def validar_correo(correo):
    """
    Valida que el correo tenga una '@' y termine en '.com'.
    Se hace con operaciones básicas de string.
    """
    # Condición 1: debe tener exactamente una arroba
    if correo.count("@") != 1:
        return False

    # Separamos en la parte antes y después del @
    partes = correo.split("@")
    parte_antes = partes[0]   # ej: "juan.perez"
    parte_despues = partes[1] # ej: "gmail.com"

    # Condición 2: la parte antes del @ no puede estar vacía
    if len(parte_antes) == 0:
        return False

    # Condición 3: debe terminar en .com
    if not parte_despues.endswith(".com"):
        return False

    # Condición 4: no puede haber espacios en el correo
    if " " in correo:
        return False

    # Condición 5: debe haber algo antes del .com (el nombre del dominio)
    dominio = parte_despues.replace(".com", "")
    if len(dominio) == 0:
        return False

    return True


# ------------------------------------------------------------------
# Función principal de registro
# ------------------------------------------------------------------

def registrar_usuario(usuarios):
    """
    Registra un nuevo usuario en el sistema.
    Cada campo tiene su propio bucle de reintento: si el dato es incorrecto,
    el programa muestra el error y vuelve a pedir ESE MISMO campo.
    Al finalizar, guarda los datos de inmediato.
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
                print("  ERROR: El nombre no puede contener números. Intente de nuevo.")

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
                print("  ERROR: El apellido no puede contener números. Intente de nuevo.")

    # --- Validar que el documento no esté ya registrado ---
    # (lo hacemos antes de pedirlo para no molestar al usuario)

    # --- Campo: Documento ---
    doc = ""
    while True:
        doc = input("Número de documento (solo números, 3-15 dígitos): ").strip()
        if not validar_documento(doc):
            if not doc.isdigit():
                print("  ERROR: El documento solo puede contener números. Intente de nuevo.")
            else:
                print("  ERROR: El documento debe tener entre 3 y 15 dígitos. Intente de nuevo.")
            continue

        # Verificar que el documento no esté duplicado
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
        correo = input("Correo electrónico (ej: nombre@dominio.com): ").strip()
        if validar_correo(correo):
            break
        else:
            print("  ERROR: Correo inválido. Debe tener '@' y terminar en '.com'. Intente de nuevo.")

    # --- Campo: Tiempo de préstamo ---
    tiempo = 0
    while True:
        print("  Opciones de tiempo: 5, 10, 15 o 30 días")
        entrada = input("  Seleccione el tiempo de préstamo: ").strip()

        # Verificamos que sea número antes de convertir
        if not entrada.isdigit():
            print("  ERROR: Debe ingresar un número. Intente de nuevo.")
            continue

        tiempo = int(entrada)

        if tiempo == 5 or tiempo == 10 or tiempo == 15 or tiempo == 30:
            break
        else:
            print("  ERROR: Tiempo no permitido. Solo se aceptan 5, 10, 15 o 30 días.")

    # --- Guardar usuario ---
    nuevo_usuario = {
        "doc": doc,
        "nombre": nombre,
        "apellido": apellido,
        "correo": correo,
        "tiempo": tiempo,
        "prestamos_realizados": 0
    }

    usuarios.append(nuevo_usuario)

    # Guardado inmediato sin esperar al menú principal
    archivos.guardar_datos(DATA_USUARIOS, usuarios)

    print(f"\n  Usuario '{nombre} {apellido}' registrado con exito! ")