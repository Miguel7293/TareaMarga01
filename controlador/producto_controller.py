import sqlite3
from modelo.database import get_db_connection
from modelo.producto import Producto

class ProductoController:
    @staticmethod
    def registrar_producto(codigo, nombre, categoria, precio, stock):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            
            # Verificar si el producto ya existe
            cursor.execute('SELECT 1 FROM productos WHERE codigo = ?', (codigo,))
            if cursor.fetchone():
                return {"exito": False, "mensaje": "El código de producto ya existe"}
            
            # Insertar nuevo producto
            cursor.execute('''
                INSERT INTO productos (codigo, nombre, categoria, precio, stock)
                VALUES (?, ?, ?, ?, ?)
            ''', (codigo, nombre, categoria, precio, stock))
            
            conn.commit()
            return {"exito": True, "mensaje": "Producto registrado exitosamente"}
        
        except sqlite3.Error as e:
            conn.rollback()
            return {"exito": False, "mensaje": f"Error de base de datos: {e}"}
        finally:
            conn.close()
    @staticmethod
    def obtener_ultimo_codigo():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT codigo FROM productos ORDER BY codigo DESC LIMIT 1")
            ultimo_codigo = cursor.fetchone()
            return ultimo_codigo[0] if ultimo_codigo else None
        finally:
            conn.close()
    @staticmethod
    def generar_nuevo_codigo():
        ultimo_codigo = ProductoController.obtener_ultimo_codigo()
        if ultimo_codigo and ultimo_codigo.startswith('P'):
            try:
                numero = int(ultimo_codigo[1:])
                return f"P{str(numero + 1).zfill(3)}"
            except ValueError:
                pass
        return "P999"  # Si no hay productos o el formato no coincide
    @staticmethod
    def listar_productos():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT codigo, nombre, precio, stock FROM productos WHERE stock > 0')
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al listar productos: {e}")
            return []
        finally:
            conn.close()
    @staticmethod
    def obtener_producto(codigo):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM productos WHERE codigo = ?', (codigo,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error al obtener producto: {e}")
            return None
        finally:
            conn.close()
