# 📘 Manual de Usuario - DataFileSolution

Bienvenido al manual oficial de **DataFileSolution**, la solución integral para la gestión de activos, préstamos y ventas automáticas.

---

## 1. Introducción
DataFileSolution es una aplicación de consola desarrollada en Python diseñada para administrar el inventario de ítems, el registro de usuarios y el control financiero de préstamos. El sistema destaca por su capacidad de procesar **ventas automáticas** cuando se exceden los tiempos de préstamo y por utilizar **lógica difusa** para evaluar la calidad de los objetos.

---

## 2. Requisitos del Sistema
* **Lenguaje:** Python 3.8 o superior.
* **Dependencias:** Ninguna (Usa librerías estándar de Python: `os`, `json`, `datetime`, `re`).
* **Estructura de Carpetas:** El sistema requiere una carpeta `src/data/` para almacenar la persistencia.

---

## 3. Guía de Inicio Rápido

### Ejecución
Para iniciar el programa, sitúese en la raíz del proyecto y ejecute:
```bash
python src/main.py

```

### Menú Principal

Al iniciar, verá un menú numerado del 0 al 6:

1. **Registrar Usuario:** Ingrese los datos del cliente (Nombre, Apellido, Documento, Correo y tiempo de préstamo).
2. **Registrar Ítem:** Ingrese el objeto al inventario. Deberá asignar puntajes de funcionalidad y estética (1-10) para que el sistema determine el estado mediante lógica difusa.
3. **Registrar Préstamo:** Seleccione un usuario registrado y un ítem disponible para iniciar un préstamo.
4. **Devolución:** Registre el retorno de un objeto y obtenga un certificado en formato `.txt` (o PDF si está implementado).
5. **Estado General:** Visualice un reporte de antigüedad de los préstamos activos.
6. **Administración:** Acceda con credenciales para ver reportes financieros.

---

## 4. Reglas de Negocio Importantes

### Validaciones de Registro

* **Nombres/Apellidos:** Mínimo 3 caracteres, no se permiten números (Soporta ñ y tildes).
* **Documento:** Entre 3 y 15 dígitos numéricos.
* **Correo:** Debe contener `@` y terminar en `.com`.
* **Tiempo:** Solo se permiten plazos de 5, 10, 15 o 30 días.

### Sistema de Ventas Automáticas (Impuesto por Conchudez)

Si un préstamo supera los **30 días calendario**, el sistema automáticamente:

1. Cambia el estado del préstamo a "Inactivo/Vendido".
2. Genera una factura de venta en la carpeta raíz.
3. Aplica el **impuesto del 23%** sobre el precio de compra original.
4. El ítem deja de estar disponible en el inventario permanentemente.

### Lógica Difusa de Estado

El estado de los ítems no se escribe manualmente. El sistema promedia la **funcionalidad (70%)** y la **estética (30%)** para clasificar el objeto en:

* Excelente
* Bueno
* Regular
* Malo

---

## 5. Módulo Administrativo

Para acceder, utilice las siguientes credenciales predeterminadas:

* **Usuario:** `admin`
* **Contraseña:** `1234`

**Reportes disponibles:**

* Total de préstamos, devoluciones y ventas.
* Recaudación total de dinero (incluyendo impuestos).
* Identificación de usuarios con mayor y menor actividad de préstamo.

---

## 6. Solución de Problemas

* **Error de Archivo No Encontrado:** Asegúrese de ejecutar el programa desde la raíz de la carpeta para que las rutas `src/data/` sean accesibles.
* **Datos no guardados:** Siempre cierre el programa usando la **Opción 0 (Guardar y Salir)** para asegurar la integridad de los archivos JSON.

---

*Manual redactado por Lina y Camila - 2026*

