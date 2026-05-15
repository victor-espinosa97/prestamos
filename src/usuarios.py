import re

def validar_nombre_apellido(texto):
    # Permite letras (incluyendo ñ y tildes) y espacios, mínimo 3 caracteres
    # Usamos un patrón que reconoce caracteres Unicode de letras
    patron = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]{3,}$"
    if re.match(patron, texto):
        # Verificamos que no sea solo espacios
        return not texto.isspace()
    return False

def validar_documento(doc):
    return doc.isdigit() and 3 <= len(doc) <= 15

def validar_correo(correo):
    # Validación específica: debe tener @ y terminar en .com
    return re.match(r'^[\w\.-]+@[\w\.-]+\.com$', correo) is not None

def registrar_usuario(usuarios):
    print("\n--- Registro de Usuario ---")
    
    nombre = input("Nombre: ")
    if not validar_nombre_apellido(nombre):
        print("Error: Nombre inválido (mínimo 3 letras, sin números).")
        return

    apellido = input("Apellido: ")
    if not validar_nombre_apellido(apellido):
        print("Error: Apellido inválido (mínimo 3 letras, sin números).")
        return

    doc = input("Documento: ")
    if not validar_documento(doc):
        print("Error: Documento inválido (solo números, entre 3 y 15 dígitos).")
        return

    correo = input("Correo electrónico: ")
    if not validar_correo(correo):
        print("Error: Correo inválido (debe incluir '@' y terminar en '.com').")
        return

    print("Opciones de tiempo de préstamo: 5, 10, 15, 30 días")
    try:
        tiempo = int(input("Seleccione tiempo: "))
        if tiempo not in [5, 10, 15, 30]:
            raise ValueError
    except ValueError:
        print("Error: Tiempo no permitido.")
        return

    usuarios.append({
        "doc": doc,
        "nombre": nombre,
        "apellido": apellido,
        "correo": correo,
        "tiempo": tiempo,
        "prestamos_realizados": 0
    })
    print(f"¡Usuario {nombre} registrado con éxito! ✔")