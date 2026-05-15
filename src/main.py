import os
import archivos
import usuarios
import items
import prestamos
import admin

# Definición de rutas de persistencia relativas a la carpeta src
DATA_DIR = "data"
DATA_USUARIOS = f"{DATA_DIR}/usuarios.json"
DATA_ITEMS = f"{DATA_DIR}/items.json"
DATA_PRESTAMOS = f"{DATA_DIR}/prestamos.json"
DATA_VENTAS = f"{DATA_DIR}/ventas.json"

def asegurar_entorno():
    """Garantiza la existencia de los directorios requeridos por el proyecto."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def limpiar_pantalla():
    """Limpia la consola para mejorar la experiencia de usuario (UX)."""
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_principal():
    """Orquestador principal de la aplicación Data File Solution."""
    # 1. Preparar el entorno de directorios
    asegurar_entorno()

    # 2. Cargar todos los datos en memoria al iniciar
    list_usuarios = archivos.cargar_datos(DATA_USUARIOS)
    list_items = archivos.cargar_datos(DATA_ITEMS)
    list_prestamos = archivos.cargar_datos(DATA_PRESTAMOS)
    list_ventas = archivos.cargar_datos(DATA_VENTAS)

    # 3. PROCESO AUTOMÁTICO: Validar ventas por mora (>30 días) antes de interactuar
    prestamos.procesar_ventas_automaticas(list_prestamos, list_items, list_ventas)

    while True:
        limpiar_pantalla()
        print("===========================================")
        print("            SISTEMA DATA FILE SOLUTION     ")
        print("        Gestión Eficiente de Activos       ")
        print("===========================================")
        print("  1. Registrar Usuario")
        print("  2. Registrar Ítem (Objeto a prestar)")
        print("  3. Registrar Préstamo")
        print("  4. Registrar y Certificar Devolución")
        print("  5. Consultar Estado General de Préstamos")
        print("  6. Panel de Administración")
        print("  0. Guardar y Salir")
        print("===========================================")
        
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            limpiar_pantalla()
            usuarios.registrar_usuario(list_usuarios)
            
        elif opcion == "2":
            limpiar_pantalla()
            items.registrar_item(list_items)
            
        elif opcion == "3":
            limpiar_pantalla()
            prestamos.registrar_prestamo(list_usuarios, list_items, list_prestamos)
            
        elif opcion == "4":
            limpiar_pantalla()
            # Esta función en prestamos.py ahora debe contener la lógica para tu PDF
            prestamos.registrar_devolucion(list_prestamos, list_items)
            
        elif opcion == "5":
            limpiar_pantalla()
            prestamos.consultar_estado_general(list_prestamos)
            
        elif opcion == "6":
            limpiar_pantalla()
            if admin.login_admin():
                admin.menu_admin(list_usuarios, list_items, list_prestamos, list_ventas)
                
        elif opcion == "0":
            print("\nGuardando datos en el sistema...")
            archivos.guardar_datos(DATA_USUARIOS, list_usuarios)
            archivos.guardar_datos(DATA_ITEMS, list_items)
            archivos.guardar_datos(DATA_PRESTAMOS, list_prestamos)
            archivos.guardar_datos(DATA_VENTAS, list_ventas)
            print("¡Datos guardados de forma segura! Hasta pronto.")
            break
            
        else:
            print("\nOpción no válida. Por favor, intente de nuevo.")
        
        # Pausa para que el usuario pueda leer los mensajes antes de limpiar la pantalla
        if opcion != "0":
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    menu_principal()