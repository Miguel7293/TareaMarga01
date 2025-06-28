import sqlite3
import os

def crear_base_datos():
    if not os.path.exists('database'):
        os.makedirs('database')
    
    conn = sqlite3.connect('database/tienda.db')
    cursor = conn.cursor()
    
    # Tabla Productos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        codigo TEXT PRIMARY KEY,
        nombre TEXT NOT NULL,
        categoria TEXT NOT NULL,
        precio REAL NOT NULL,
        stock INTEGER NOT NULL
    )
    ''')
    
    # Tabla Ventas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total REAL NOT NULL
    )
    ''')
    
    # Tabla DetalleVenta
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS detalle_venta (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venta_id INTEGER NOT NULL,
        producto_codigo TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        precio_unitario REAL NOT NULL,
        subtotal REAL NOT NULL,
        FOREIGN KEY (venta_id) REFERENCES ventas(id),
        FOREIGN KEY (producto_codigo) REFERENCES productos(codigo)
    )
    ''')
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insertar productos iniciales solo si no existen
    productos_iniciales = [
        {'codigo': 'P001', 'nombre': 'Arroz 1kg', 'categoria': 'Abarrotes', 'precio': 3.50, 'stock': 100},
        {'codigo': 'P002', 'nombre': 'Leche entera 1L', 'categoria': 'Lácteos', 'precio': 4.20, 'stock': 80},
        {'codigo': 'P003', 'nombre': 'Atún en lata', 'categoria': 'Conservas', 'precio': 5.80, 'stock': 50},
        {'codigo': 'P004', 'nombre': 'Jabón de baño', 'categoria': 'Aseo', 'precio': 2.30, 'stock': 120},
        {'codigo': 'P005', 'nombre': 'Coca-Cola 2L', 'categoria': 'Bebidas', 'precio': 7.50, 'stock': 60},
        {'codigo': 'P006', 'nombre': 'Galletas de chocolate', 'categoria': 'Golosinas', 'precio': 3.20, 'stock': 75},
        {'codigo': 'P007', 'nombre': 'Papel higiénico 4rollos', 'categoria': 'Aseo', 'precio': 6.40, 'stock': 90},
        {'codigo': 'P008', 'nombre': 'Huevos x12', 'categoria': 'Lácteos', 'precio': 8.00, 'stock': 60},
        {'codigo': 'P009', 'nombre': 'Aceite vegetal 1L', 'categoria': 'Abarrotes', 'precio': 9.50, 'stock': 40},
        {'codigo': 'P010', 'nombre': 'Pan integral', 'categoria': 'Panadería', 'precio': 4.50, 'stock': 30}
    ]
    
    for producto in productos_iniciales:
        # Verificar si el producto ya existe
        cursor.execute('SELECT 1 FROM productos WHERE codigo = ?', (producto['codigo'],))
        if not cursor.fetchone():
            cursor.execute('''
            INSERT INTO productos (codigo, nombre, categoria, precio, stock)
            VALUES (?, ?, ?, ?, ?)
            ''', (producto['codigo'], producto['nombre'], producto['categoria'], 
                 producto['precio'], producto['stock']))
    
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect('database/tienda.db')