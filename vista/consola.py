from modelo.producto import Producto
def mostrar_menu_principal():
    print("\n--- SISTEMA DE CAJA REGISTRADORA ---")
    print("1. Nueva venta")
    print("2. Listar productos")
    print("3. Registrar nuevo producto")
    print("4. Eliminar producto")  
    print("5. Ver historial de ventas")
    print("6. Salir")
    
    try:
        opcion = int(input("Seleccione una opción: "))
        return opcion
    except ValueError:
        print("Error: Ingrese un número válido")
        return -1

def mostrar_opcion_eliminar():
    print("\n--- ELIMINAR PRODUCTO ---")
    codigo = input("Ingrese código del producto a eliminar: ").strip().upper()
    return codigo
def mostrar_formulario_producto():
    print("\n--- REGISTRAR NUEVO PRODUCTO ---")
    
    # Nombre (requerido)
    while True:
        nombre = input("Nombre del producto: ").strip()
        if nombre:
            break
        print("El nombre no puede estar vacío")

    # Categoría (requerido)
    while True:
        categoria = input("Categoría: ").strip()
        if categoria:
            break
        print("La categoría no puede estar vacía")

    # Precio (número positivo)
    while True:
        try:
            precio = float(input("Precio unitario: "))
            if precio > 0:
                break
            print("El precio debe ser mayor a 0")
        except ValueError:
            print("Error: Ingrese un número válido")

    # Stock (entero positivo)
    while True:
        try:
            stock = int(input("Stock inicial: "))
            if stock >= 0:
                break
            print("El stock no puede ser negativo")
        except ValueError:
            print("Error: Ingrese un número entero válido")

    return nombre, categoria, precio, stock

def mostrar_productos(productos):
    print("\n--- LISTADO DE PRODUCTOS ---")
    print("{:<10} {:<20} {:<15} {:<10} {:<10}".format(
        "Código", "Nombre", "Categoría", "Precio", "Stock"))
    print("-" * 65)
    for prod in productos:
        try:
            # Convertir el precio a float antes de formatear
            precio = float(prod[3])
            print("{:<10} {:<20} {:<15} ${:<9.2f} {:<10}".format(
                prod[0], prod[1], prod[2], precio, prod[4]))
        except (ValueError, TypeError, IndexError) as e:
            print(f"Error mostrando producto {prod}: {str(e)}")
            continue

def mostrar_mensaje(mensaje):
    print(f"\n{mensaje}")

def capturar_venta():
    print("\n--- NUEVA VENTA ---")
    print("(Ingrese 'fin' para terminar o 'cancelar' para anular la venta)\n")
    items = []
    
    while True:
        codigo = input("Ingrese código de producto: ").strip()
        
        # Opciones especiales
        if codigo.lower() == 'fin':
            break
        if codigo.lower() == 'cancelar':
            return None  # Retorna None para indicar venta cancelada
            
        producto = Producto.obtener_por_codigo(codigo)
        if not producto:
            print("\n⚠️ Producto no encontrado ⚠️")
            continue
            
        # Mostrar detalles del producto encontrado
        print("\n----------------------------------------")
        print(f"PRODUCTO ENCONTRADO:")
        print(f"Código: {producto[0]}")
        print(f"Nombre: {producto[1]}")
        print(f"Categoría: {producto[2]}")
        print(f"Precio unitario: ${producto[3]:.2f}")
        print(f"Stock disponible: {producto[4]}")
        print("----------------------------------------")
        
        # Confirmación del producto
        confirmacion = input("\n¿Es este el producto correcto? (S/N): ").strip().lower()
        if confirmacion != 's':
            print("Producto no añadido. Intente con otro código.")
            continue
            
        # Captura de cantidad
        while True:
            try:
                cantidad = int(input("\nIngrese cantidad: "))
                if cantidad <= 0:
                    print("La cantidad debe ser mayor a 0")
                    continue
                if cantidad > producto[4]:
                    print(f"⚠️ No hay suficiente stock. Disponible: {producto[4]}")
                    continue
                break
            except ValueError:
                print("Error: Ingrese un número entero válido")
        
        # Calcular subtotal
        subtotal = cantidad * producto[3]
        items.append({
            'codigo': producto[0],
            'nombre': producto[1],
            'precio': producto[3],
            'cantidad': cantidad,
            'subtotal': subtotal
        })
        
        print(f"\n✅ Añadido: {cantidad} x {producto[1]} = ${subtotal:.2f}")
        print(f"Total parcial: ${sum(item['subtotal'] for item in items):.2f}\n")
    
    return items if items else None

def mostrar_resumen_venta(items):
    print("\n--- RESUMEN DE VENTA ---")
    print("{:<5} {:<20} {:<10} {:<10}".format(
        "Cant.", "Producto", "P.Unit.", "Subtotal"))
    print("-" * 55)
    
    total = 0
    for item in items:
        print("{:<5} {:<20} ${:<9.2f} ${:<9.2f}".format(
            item['cantidad'], item['nombre'], item['precio'], item['subtotal']))
        total += item['subtotal']
    
    print("-" * 55)
    print(f"TOTAL: ${total:.2f}")
    return total

def mostrar_historial_ventas(ventas):
    print("\n--- HISTORIAL DE VENTAS ---")
    print("{:<5} {:<20} {:<10}".format("ID", "Fecha", "Total"))
    print("-" * 40)
    
    for registro in ventas:
        try:
            # Versión defensiva que maneja cualquier orden
            id_venta = registro[0]
            
            # Intenta determinar qué campo es el total y cuál la fecha
            campo1, campo2 = registro[1], registro[2]
            
            if isinstance(campo1, (float, int)) or (isinstance(campo1, str) and campo1.replace('.', '').isdigit()):
                total = float(campo1)
                fecha = str(campo2)[:19]
            else:
                total = float(campo2)
                fecha = str(campo1)[:19]
            
            print(f"{id_venta:<5} {fecha:<20} ${total:<9.2f}")
            
        except Exception as e:
            print(f"Error mostrando registro {registro}: {str(e)}")
            continue