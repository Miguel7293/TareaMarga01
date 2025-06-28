from modelo.database import crear_base_datos
from controlador.producto_controller import ProductoController
from controlador.venta_controller import VentaController
from vista.consola import mostrar_menu_principal, mostrar_mensaje

def main():
    # Inicializar base de datos
    crear_base_datos()
    
    while True:
        opcion = mostrar_menu_principal()
        
        if opcion == 1:
            VentaController.nueva_venta()
        elif opcion == 2:
            ProductoController.listar_productos()
        elif opcion == 3:
            ProductoController.registrar_producto()
        elif opcion == 4:  
            ProductoController.eliminar_producto()
        elif opcion == 5:
            VentaController.listar_ventas()
        elif opcion == 6:
            mostrar_mensaje("Saliendo del sistema...")
            break
        else:
            mostrar_mensaje("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()