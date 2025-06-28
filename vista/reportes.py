from datetime import datetime
import os
from fpdf import FPDF

def generar_boleta_pdf(venta_id, cabecera, detalles):
    pdf = FPDF()
    pdf.add_page()
    
    # Configuración inicial
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Miguel's Store", 0, 1, 'C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, "Boleta de Venta", 0, 1, 'C')
    pdf.cell(0, 10, f"N° {venta_id}", 0, 1, 'C')
    
    # Manejo seguro de la fecha
    try:
        # Verificar si cabecera es una tupla/lista con al menos 3 elementos
        if isinstance(cabecera, (tuple, list)) and len(cabecera) >= 3:
            fecha_str = str(cabecera[2])  # Convertir a string por si acaso
            fecha = fecha_str[:19] if fecha_str else "Fecha no disponible"
        else:
            fecha = "Fecha no disponible"
    except Exception as e:
        print(f"Error al obtener fecha: {e}")
        fecha = "Fecha no disponible"
    
    pdf.cell(0, 10, f"Fecha: {fecha}", 0, 1, 'C')
    pdf.ln(10)
    
    # Resto del código permanece igual...
    # Encabezado de tabla
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(20, 10, "Cant.", 1, 0, 'C')
    pdf.cell(100, 10, "Producto", 1, 0, 'C')
    pdf.cell(30, 10, "P.Unit.", 1, 0, 'C')
    pdf.cell(30, 10, "Subtotal", 1, 1, 'C')
    
    # Detalles
    pdf.set_font("Arial", '', 10)
    for detalle in detalles:
        try:
            pdf.cell(20, 10, str(detalle[3]), 1, 0, 'C')
            pdf.cell(100, 10, detalle[6], 1, 0)
            pdf.cell(30, 10, f"${float(detalle[4]):.2f}", 1, 0, 'R')
            pdf.cell(30, 10, f"${float(detalle[5]):.2f}", 1, 1, 'R')
        except Exception as e:
            print(f"Error al procesar detalle: {e}")
            continue
    
    # Cálculo del total con manejo de errores
    try:
        if isinstance(cabecera, (tuple, list)) and len(cabecera) >= 2:
            total = float(cabecera[1])
        else:
            total = sum(float(d[5]) for d in detalles)
    except Exception as e:
        print(f"Error al calcular total: {e}")
        total = 0.0
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(150, 10, "TOTAL:", 1, 0, 'R')
    pdf.cell(30, 10, f"${total:.2f}", 1, 1, 'R')
    
    # Guardar PDF
    if not os.path.exists('boletas'):
        os.makedirs('boletas')
    nombre_archivo = f"boletas/boleta_{venta_id}.pdf"
    pdf.output(nombre_archivo)
    
    return nombre_archivo