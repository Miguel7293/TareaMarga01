from modelo.producto import Producto
from modelo.venta import Venta
from vista.consola import capturar_venta, mostrar_resumen_venta, mostrar_mensaje,mostrar_historial_ventas
from vista.reportes import generar_boleta_pdf

class VentaController:
    @staticmethod
    def nueva_venta():
        items = capturar_venta()
        
        if not items:
            mostrar_mensaje("Venta cancelada. No se agregaron productos.")
            return
        
        total = mostrar_resumen_venta(items)
        
        confirmacion = input("\nConfirmar venta (s/n): ").lower()
        if confirmacion != 's':
            mostrar_mensaje("Venta cancelada.")
            return
        
        # Preparar detalles para la base de datos
        detalles_db = []
        for item in items:
            detalles_db.append({
                'codigo': item['codigo'],
                'cantidad': item['cantidad'],
                'precio': item['precio'],
                'subtotal': item['subtotal']
            })
        
        # Registrar venta
        venta_id = Venta.registrar_venta(total, detalles_db)
        
        # Generar boleta
        venta_completa = Venta.obtener_venta(venta_id)
        boleta_path = generar_boleta_pdf(
            venta_id, 
            venta_completa['cabecera'], 
            venta_completa['detalles']
        )
        
        mostrar_mensaje(f"Venta registrada exitosamente! ID: {venta_id}")
        mostrar_mensaje(f"Boleta generada en: {boleta_path}")

    @staticmethod
    def listar_ventas():
        ventas = Venta.listar_ventas()
        if not ventas:
            mostrar_mensaje("No hay ventas registradas.")
            return
        
        mostrar_historial_ventas(ventas)