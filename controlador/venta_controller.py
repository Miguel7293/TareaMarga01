import sqlite3
from modelo.database import get_db_connection
from modelo.producto import Producto
from modelo.venta import Venta

class VentaController:
    @staticmethod
    def obtener_venta_por_id(venta_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, fecha, total 
                FROM ventas 
                WHERE id = ?
            """, (venta_id,))
            venta = cursor.fetchone()
            return dict(venta) if venta else None
        finally:
            conn.close()

    @staticmethod
    def obtener_detalle_venta(venta_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.nombre, dv.cantidad, dv.precio_unitario, dv.subtotal
                FROM detalle_venta dv
                JOIN productos p ON dv.producto_codigo = p.codigo
                WHERE dv.venta_id = ?
            """, (venta_id,))
            detalles = cursor.fetchall()
            return [dict(detalle) for detalle in detalles]
        finally:
            conn.close()
    @staticmethod
    def listar_ventas():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT v.id, v.fecha, v.total, 
                       GROUP_CONCAT(p.nombre, ', ') AS productos,
                       GROUP_CONCAT(dv.cantidad, ', ') AS cantidades
                FROM ventas v
                JOIN detalle_venta dv ON v.id = dv.venta_id
                JOIN productos p ON dv.producto_codigo = p.codigo
                GROUP BY v.id
                ORDER BY v.fecha DESC
            ''')
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al listar ventas: {e}")
            return []
        finally:
            conn.close()
    
    @staticmethod
    def registrar_venta(productos):
        """
        productos: lista de diccionarios con {codigo, cantidad}
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            
            # Calcular el total de la venta
            total = 0
            detalles = []
            
            # Verificar stock y calcular total
            for item in productos:
                cursor.execute('SELECT precio, stock FROM productos WHERE codigo = ?', (item['codigo'],))
                producto = cursor.fetchone()
                
                if not producto:
                    return {"exito": False, "mensaje": f"Producto {item['codigo']} no encontrado"}
                
                precio, stock = producto
                if stock < item['cantidad']:
                    return {"exito": False, "mensaje": f"Stock insuficiente para producto {item['codigo']}"}
                
                subtotal = precio * item['cantidad']
                total += subtotal
                detalles.append({
                    'codigo': item['codigo'],
                    'cantidad': item['cantidad'],
                    'precio': precio,
                    'subtotal': subtotal
                })
            
            # Registrar la venta
            cursor.execute('INSERT INTO ventas (total) VALUES (?)', (total,))
            venta_id = cursor.lastrowid
            
            # Registrar detalles de venta y actualizar stock
            for detalle in detalles:
                cursor.execute('''
                    INSERT INTO detalle_venta 
                    (venta_id, producto_codigo, cantidad, precio_unitario, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                ''', (venta_id, detalle['codigo'], detalle['cantidad'], 
                     detalle['precio'], detalle['subtotal']))
                
                cursor.execute('''
                    UPDATE productos 
                    SET stock = stock - ? 
                    WHERE codigo = ?
                ''', (detalle['cantidad'], detalle['codigo']))
            
            conn.commit()
            return {"exito": True, "mensaje": "Venta registrada exitosamente", "venta_id": venta_id}
            
        except sqlite3.Error as e:
            conn.rollback()
            return {"exito": False, "mensaje": f"Error al registrar venta: {e}"}
        finally:
            conn.close()