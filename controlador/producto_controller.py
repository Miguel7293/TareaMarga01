from modelo.producto import Producto
from vista.consola import mostrar_formulario_producto, mostrar_productos, mostrar_mensaje,mostrar_opcion_eliminar

class ProductoController:
    @staticmethod
    def registrar_producto():
        datos = mostrar_formulario_producto()
        if Producto.agregar_producto(*datos):
            mostrar_mensaje("Producto registrado exitosamente!")
        else:
            mostrar_mensaje("Error al registrar producto")
    @staticmethod
    def eliminar_producto():
        codigo = mostrar_opcion_eliminar()
        if Producto.eliminar_producto(codigo):
            mostrar_mensaje(f"Producto {codigo} eliminado correctamente")
        else:
            mostrar_mensaje("No se pudo eliminar el producto (¿código válido?)")
    @staticmethod
    def listar_productos():
        productos = Producto.listar_productos()
        mostrar_productos(productos)