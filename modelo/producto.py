from .database import get_db_connection
import sqlite3

class Producto:
    @staticmethod
    def crear_tabla():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            codigo TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL CHECK(precio >= 0),
            stock INTEGER NOT NULL CHECK(stock >= 0)
        )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def generar_codigo():
        """Genera código autoincremental P001, P002,..."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(CAST(SUBSTR(codigo, 2) AS INTEGER)) FROM productos')
        max_num = cursor.fetchone()[0] or 0
        conn.close()
        return f"P{max_num + 1:03d}"  # Formato P001, P002,...

    @staticmethod
    def agregar_producto(nombre, categoria, precio, stock):
        """Versión segura con validación de tipos"""
        try:
            # Validaciones
            if not isinstance(nombre, str) or not nombre.strip():
                raise ValueError("Nombre inválido")
            if not isinstance(categoria, str) or not categoria.strip():
                raise ValueError("Categoría inválida")
            precio = float(precio)
            stock = int(stock)
            if precio < 0 or stock < 0:
                raise ValueError("Precio y stock deben ser positivos")

            codigo = Producto.generar_codigo()
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO productos (codigo, nombre, categoria, precio, stock)
            VALUES (?, ?, ?, ?, ?)
            ''', (codigo, nombre.strip(), categoria.strip(), precio, stock))
            conn.commit()
            return True
        except ValueError as e:
            print(f"Error de validación: {e}")
            return False
        except sqlite3.Error as e:
            print(f"Error de base de datos: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar_producto(codigo):
        """Elimina un producto por su código"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM productos WHERE codigo = ?', (codigo,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al eliminar: {e}")
            return False
        finally:
            conn.close()
    @staticmethod
    def obtener_por_codigo(codigo):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos WHERE codigo = ?', (codigo,))
        producto = cursor.fetchone()
        conn.close()
        return producto

    @staticmethod
    def listar_productos():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT codigo, nombre, categoria, precio, stock FROM productos')
        productos = cursor.fetchall()
        conn.close()
        return productos

    @staticmethod
    def actualizar_stock(codigo, cantidad):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE productos 
        SET stock = stock - ? 
        WHERE codigo = ? AND stock >= ?
        ''', (cantidad, codigo, cantidad))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return affected > 0