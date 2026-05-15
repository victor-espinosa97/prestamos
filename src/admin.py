import os

def limpiar_pantalla():
    # Limpia la consola según el sistema operativo
    os.system('cls' if os.name == 'nt' else 'clear')

def login_admin():
    """Validación de acceso con credenciales protegidas."""
    # En una app real, esto iría cifrado, pero para el proyecto académico usamos un dict
    credenciales = {
        "admin": "1234",
        "lina.duque": "udea2026",
        "camila": "udea2026"
    }
    
    print("\n" + "="*30)
    print("      ACCESO RESTRINGIDO")
    print("="*30)
    usuario = input("Usuario: ").strip()
    clave = input("Contraseña: ").strip()
    
    if credenciales.get(usuario) == clave:
        return True
    
    print("\033[91mError: Credenciales no válidas.\033[0m") # Texto en rojo
    return False

def mostrar_lista_usuarios(usuarios):
    print(f"\n{'DOCUMENTO':<15} | {'NOMBRE COMPLETO':<30} | {'PRESTAMOS'}")
    print("-" * 60)
    for u in usuarios:
        nombre = f"{u['nombre']} {u['apellido']}"
        print(f"{u['doc']:<15} | {nombre[:30]:<30} | {u['prestamos_realizados']}")

def determinar_extremos_usuarios(usuarios):
    if not usuarios:
        print("No hay usuarios para analizar.")
        return

    # Usamos funciones de orden superior para eficiencia
    u_max = max(usuarios, key=lambda x: x['prestamos_realizados'])
    u_min = min(usuarios, key=lambda x: x['prestamos_realizados'])

    print(f"\n🏆 Usuario con mayor cantidad de préstamos: {u_max['nombre']} {u_max['apellido']} ({u_max['prestamos_realizados']})")
    print(f"📉 Usuario con menor cantidad de préstamos: {u_min['nombre']} {u_min['apellido']} ({u_min['prestamos_realizados']})")

def mostrar_reportes_financieros(prestamos, ventas):
    # Lógica de cálculo de métricas
    total_prestamos = len(prestamos)
    total_devueltos = len([p for p in prestamos if not p['activo']])
    total_ventas = len(ventas)
    
    # Recaudación: Suma de subtotales + impuestos
    recaudo_total = sum(v['total'] for v in ventas)
    
    print(f"\n--- MÉTRICAS GENERALES ---")
    print(f"✅ Total de préstamos registrados: {total_prestamos}")
    print(f"📦 Total de ítems devueltos:       {total_devueltos}")
    print(f"💰 Total de ventas realizadas:     {total_ventas}")
    print(f"💵 Total pago realizado (Recaudo): ${recaudo_total:,.2f}")

def menu_admin(usuarios, items, prestamos, ventas):
    """Controlador principal del submódulo administrativo."""
    while True:
        print("\n" + "╔" + "═"*38 + "╗")
        print("║      PANEL DE CONTROL ADMINISTRATIVO   ║")
        print("╚" + "═"*38 + "╝")
        print("1. Ver Reporte de Métricas Totales")
        print("2. Ver Lista de Usuarios Registrados")
        print("3. Ver Usuario Líder vs Usuario Menor")
        print("0. Salir al Menú Principal")
        
        opcion = input("\nSeleccione reporte: ")

        if opcion == "1":
            limpiar_pantalla()
            mostrar_reportes_financieros(prestamos, ventas)
        elif opcion == "2":
            limpiar_pantalla()
            mostrar_lista_usuarios(usuarios)
        elif opcion == "3":
            limpiar_pantalla()
            determinar_extremos_usuarios(usuarios)
        elif opcion == "0":
            print("Saliendo del panel administrativo...")
            break
        else:
            print("Opción no válida.")
        
        input("\nPresione Enter para continuar...")
        limpiar_pantalla()