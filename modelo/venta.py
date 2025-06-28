from .database import get_db_connection
from datetime import datetime

class Venta:
    @staticmethod
    def registrar_venta(total, detalles):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Registrar la venta principal
        cursor.execute('''
        INSERT INTO ventas (total, fecha)
        VALUES (?, ?)
        ''', (total, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        venta_id = cursor.lastrowid
        
        # Registrar los detalles de la venta
        for detalle in detalles:
            cursor.execute('''
            INSERT INTO detalle_venta (venta_id, producto_codigo, cantidad, precio_unitario, subtotal)
            VALUES (?, ?, ?, ?, ?)
            ''', (venta_id, detalle['codigo'], detalle['cantidad'], detalle['precio'], detalle['subtotal']))
            
            # Actualizar stock
            cursor.execute('''
            UPDATE productos 
            SET stock = stock - ? 
            WHERE codigo = ?
            ''', (detalle['cantidad'], detalle['codigo']))
        
        conn.commit()
        conn.close()
        return venta_id

    @staticmethod
    def obtener_venta(venta_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Obtener cabecera de venta
        cursor.execute('SELECT * FROM ventas WHERE id = ?', (venta_id,))
        venta = cursor.fetchone()
        
        if not venta:
            return None
        
        # Obtener detalles
        cursor.execute('''
        SELECT dv.*, p.nombre 
        FROM detalle_venta dv
        JOIN productos p ON dv.producto_codigo = p.codigo
        WHERE dv.venta_id = ?
        ''', (venta_id,))
        detalles = cursor.fetchall()
        
        conn.close()
        
        return {
            'cabecera': venta,
            'detalles': detalles
        }

    @staticmethod
    def listar_ventas():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Asegúrate de que el orden de los campos sea CORRECTO: id, total, fecha
        cursor.execute('SELECT id, total, fecha FROM ventas ORDER BY fecha DESC')
        ventas = cursor.fetchall()
        
        # Depuración: Ver estructura de los datos
        print("Ejemplo de registro:", ventas[0] if ventas else "No hay ventas")
        
        conn.close()
        return ventas