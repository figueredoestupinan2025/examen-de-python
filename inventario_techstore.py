"""
Sistema de Gestión de Inventario para TechStore
Gestiona productos con validación completa y persistencia de datos.
"""

import json
import os

ARCHIVO_INVENTARIO = "inventario.json"


def cargar_inventario():
    """
    Carga el inventario desde el archivo JSON.
    Si el archivo no existe, crea una lista vacía.
    """
    try:
        with open(ARCHIVO_INVENTARIO, 'r', encoding='utf-8') as archivo:
            inventario = json.load(archivo)
            print("✓ Inventario cargado correctamente.")
            return inventario
    except FileNotFoundError:
        print("⚠ No se encontró el archivo de inventario. Se creará uno nuevo.")
        return []
    except json.JSONDecodeError:
        print("⚠ El archivo de inventario está corrupto. Se creará uno nuevo.")
        return []
    except Exception as e:
        print(f"⚠ Error al cargar el inventario: {e}. Se creará uno nuevo.")
        return []


def guardar_inventario(inventario):
    """
    Guarda el inventario en el archivo JSON.
    """
    try:
        with open(ARCHIVO_INVENTARIO, 'w', encoding='utf-8') as archivo:
            json.dump(inventario, archivo, indent=4, ensure_ascii=False)
        print("✓ Inventario guardado correctamente.")
    except Exception as e:
        print(f"⚠ Error al guardar el inventario: {e}")


def validar_numero_positivo(mensaje, tipo=float):
    """
    Solicita un número positivo al usuario.
    tipo: puede ser float o int
    """
    while True:
        try:
            valor = tipo(input(mensaje))
            if valor < 0:
                print("⚠ El valor no puede ser negativo. Intente nuevamente.")
                continue
            return valor
        except ValueError:
            print("⚠ Error: Debe ingresar un número válido.")


def agregar_producto(inventario):
    """
    Agrega un nuevo producto al inventario.
    """
    print("\n--- AGREGAR PRODUCTO ---")
    
    # Solicitar nombre
    nombre = input("Nombre del producto: ").strip()
    if not nombre:
        print("⚠ El nombre no puede estar vacío.")
        return
    
    # Verificar si el producto ya existe
    for producto in inventario:
        if producto['nombre'].lower() == nombre.lower():
            print(f"⚠ El producto '{nombre}' ya existe en el inventario.")
            return
    
    # Solicitar precio y cantidad con validación
    precio = validar_numero_positivo("Precio del producto: $", float)
    cantidad = validar_numero_positivo("Cantidad en stock: ", int)
    
    # Crear nuevo producto
    nuevo_producto = {
        'nombre': nombre,
        'precio': precio,
        'cantidad': cantidad
    }
    
    inventario.append(nuevo_producto)
    print(f"✓ Producto '{nombre}' agregado exitosamente.")


def actualizar_stock(inventario):
    """
    Actualiza la cantidad de un producto existente.
    """
    print("\n--- ACTUALIZAR STOCK ---")
    
    if not inventario:
        print("⚠ El inventario está vacío.")
        return
    
    # Buscar producto por nombre
    nombre_buscar = input("Nombre del producto a buscar: ").strip()
    
    for producto in inventario:
        if producto['nombre'].lower() == nombre_buscar.lower():
            print(f"Producto encontrado: {producto['nombre']}")
            print(f"Stock actual: {producto['cantidad']}")
            
            # Solicitar nueva cantidad
            nueva_cantidad = validar_numero_positivo("Nueva cantidad: ", int)
            producto['cantidad'] = nueva_cantidad
            
            print(f"✓ Stock de '{producto['nombre']}' actualizado a {nueva_cantidad} unidades.")
            return
    
    print(f"⚠ No se encontró el producto '{nombre_buscar}' en el inventario.")


def mostrar_inventario(inventario):
    """
    Muestra todos los productos del inventario.
    """
    print("\n--- INVENTARIO ACTUAL ---")
    
    if not inventario:
        print("⚠ El inventario está vacío. Agregue productos primero.")
        return
    
    # Calcular valor total del inventario
    valor_total = sum(p['precio'] * p['cantidad'] for p in inventario)
    
    print(f"{'N°':<4} {'NOMBRE':<20} {'PRECIO':<12} {'CANTIDAD':<10}")
    print("-" * 46)
    
    for indice, producto in enumerate(inventario, 1):
        print(f"{indice:<4} {producto['nombre']:<20} ${producto['precio']:<11.2f} {producto['cantidad']:<10}")
    
    print("-" * 46)
    print(f"Total de productos: {len(inventario)}")
    print(f"Valor total del inventario: ${valor_total:.2f}")


def mostrar_menu():
    """
    Muestra el menú de opciones.
    """
    print("\n" + "=" * 50)
    print("         SISTEMA DE GESTIÓN DE INVENTARIO")
    print("                   TechStore")
    print("=" * 50)
    print("1. Cargar Inventario")
    print("2. Agregar Producto")
    print("3. Actualizar Stock")
    print("4. Mostrar Inventario")
    print("5. Guardar y Salir")
    print("=" * 50)


def obtener_opcion():
    """
    Solicita y valida la opción del menú.
    """
    while True:
        try:
            opcion = int(input("\nSeleccione una opción (1-5): "))
            if 1 <= opcion <= 5:
                return opcion
            else:
                print("⚠ Opción inválida. Debe ser entre 1 y 5.")
        except ValueError:
            print("⚠ Error: Debe ingresar un número válido.")


def ejecutar_opcion(opcion, inventario):
    """
    Ejecuta la opción seleccionada por el usuario.
    Retorna True si debe continuar el programa, False si debe salir.
    """
    if opcion == 1:
        # Recargar inventario
        inventario = cargar_inventario()
        return True, inventario
    
    elif opcion == 2:
        agregar_producto(inventario)
        return True, inventario
    
    elif opcion == 3:
        actualizar_stock(inventario)
        return True, inventario
    
    elif opcion == 4:
        mostrar_inventario(inventario)
        return True, inventario
    
    elif opcion == 5:
        print("\n--- GUARDAR Y SALIR ---")
        guardar_inventario(inventario)
        print("¡Gracias por usar el sistema de TechStore!")
        return False, inventario


def main():
    """
    Función principal del programa.
    """
    print("¡Bienvenido al Sistema de Gestión de Inventario de TechStore!")
    
    # Cargar inventario al inicio
    inventario = cargar_inventario()
    
    # Ciclo principal del programa
    continuar = True
    
    while continuar:
        mostrar_menu()
        opcion = obtener_opcion()
        continuar, inventario = ejecutar_opcion(opcion, inventario)


if __name__ == "__main__":
    main()

