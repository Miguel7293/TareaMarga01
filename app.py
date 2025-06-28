from flask import Flask, render_template, request, redirect, url_for, flash
from controlador.producto_controller import ProductoController
from controlador.venta_controller import VentaController
from flask import make_response
from fpdf import FPDF
import io

app = Flask(__name__, template_folder='vista/templates')

@app.route('/')
def inicio():
    return render_template('inicio.html')

# Rutas para Productos
@app.route('/productos')
def listar_productos():
    productos = ProductoController.listar_productos()
    return render_template('productos.html', productos=productos)

@app.route('/registrar-producto', methods=['GET', 'POST'])
def registrar_producto():
    if request.method == 'POST':
        try:
            codigo = request.form['codigo']
            nombre = request.form['nombre']
            categoria = request.form['categoria']
            precio = float(request.form['precio'])
            stock = int(request.form['stock'])
            
            resultado = ProductoController.registrar_producto(
                codigo, nombre, categoria, precio, stock
            )
            
            if resultado['exito']:
                flash("Producto registrado exitosamente", "success")
                return redirect(url_for('nueva_venta', nuevo_producto=codigo))
            flash(resultado['mensaje'], "danger")
        except Exception as e:
            flash(f"Error al registrar producto: {str(e)}", "danger")
    
    nuevo_codigo = ProductoController.generar_nuevo_codigo()
    return render_template('registrar_producto.html', nuevo_codigo=nuevo_codigo)

@app.route('/editar-producto', methods=['GET', 'POST'])
def editar_producto(codigo):
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            categoria = request.form['categoria']
            precio = float(request.form['precio'])
            stock = int(request.form['stock'])
            
            resultado = ProductoController.actualizar_producto(
                codigo, nombre, categoria, precio, stock
            )
            
            flash(resultado['mensaje'], 'success' if resultado['exito'] else 'danger')
            return redirect(url_for('listar_productos'))
        
        except Exception as e:
            flash(f"Error al actualizar producto: {str(e)}", "danger")
            return redirect(url_for('editar_producto', codigo=codigo))
    
    producto = ProductoController.obtener_producto(codigo)
    if not producto:
        flash("Producto no encontrado", "danger")
        return redirect(url_for('listar_productos'))
    
    return render_template('editar_producto.html', producto=producto)

@app.route('/eliminar-producto')
def eliminar_producto(codigo):
    resultado = ProductoController.eliminar_producto(codigo)
    flash(resultado['mensaje'], 'success' if resultado['exito'] else 'danger')
    return redirect(url_for('listar_productos'))

@app.route('/nueva-venta', methods=['GET', 'POST'])
def nueva_venta():
    if request.method == 'POST':
        try:
            productos = []
            i = 1
            while True:
                codigo = request.form.get(f'producto_{i}_codigo')
                if not codigo:
                    break
                cantidad = int(request.form.get(f'producto_{i}_cantidad', 0))
                if cantidad > 0:
                    productos.append({'codigo': codigo, 'cantidad': cantidad})
                i += 1
            
            if not productos:
                flash("Debe agregar al menos un producto", "danger")
                return redirect(url_for('nueva_venta'))
            
            resultado = VentaController.registrar_venta(productos)
            if resultado['exito']:
                flash("Venta registrada exitosamente", "success")
                # Redirigir a la misma página pero con opción de PDF
                return render_template('nueva_venta.html', 
                                     productos=ProductoController.listar_productos(),
                                     venta_completada=True,
                                     venta_id=resultado['venta_id'])
            else:
                flash(resultado['mensaje'], "danger")
            
        except Exception as e:
            flash(f"Error al procesar la venta: {str(e)}", "danger")
    
    productos = ProductoController.listar_productos()
    return render_template('nueva_venta.html', productos=productos)

@app.route('/historial-ventas')
def historial_ventas():
    ventas = VentaController.listar_ventas()
    return render_template('historial_ventas.html', ventas=ventas)

@app.route('/detalle-venta/<int:venta_id>')
def detalle_venta(venta_id):
    detalle = VentaController.obtener_detalle_venta(venta_id)
    if not detalle:
        flash("Venta no encontrada", "danger")
        return redirect(url_for('historial_ventas'))
    
    return render_template('detalle_venta.html', detalle=detalle)
@app.route('/generar-pdf/<int:venta_id>')
def generar_pdf(venta_id):
    # Obtener datos de la venta
    venta = VentaController.obtener_venta_por_id(venta_id)
    detalles = VentaController.obtener_detalle_venta(venta_id)
    
    if not venta or not detalles:
        flash("Venta no encontrada", "danger")
        return redirect(url_for('historial_ventas'))
    
    # Crear PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Encabezado
    pdf.cell(200, 10, txt="Comprobante de Venta", ln=1, align='C')
    pdf.cell(200, 10, txt=f"Venta N° {venta_id}", ln=1, align='C')
    pdf.cell(200, 10, txt=f"Fecha: {venta['fecha']}", ln=1, align='C')
    pdf.ln(10)
    
    # Detalles
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(40, 10, "Producto", border=1)
    pdf.cell(30, 10, "Precio", border=1)
    pdf.cell(30, 10, "Cantidad", border=1)
    pdf.cell(40, 10, "Subtotal", border=1, ln=1)
    pdf.set_font("Arial", size=10)
    
    for detalle in detalles:
        pdf.cell(40, 10, detalle['nombre'], border=1)
        pdf.cell(30, 10, f"S/ {detalle['precio_unitario']:.2f}", border=1)
        pdf.cell(30, 10, str(detalle['cantidad']), border=1)
        pdf.cell(40, 10, f"S/ {detalle['subtotal']:.2f}", border=1, ln=1)
    
    # Total
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(100, 10, "TOTAL:", 0, 0, 'R')
    pdf.cell(40, 10, f"S/ {venta['total']:.2f}", 0, 1)
    
    # Generar respuesta
    pdf_output = pdf.output(dest='S').encode('latin1')
    response = make_response(pdf_output)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=venta_{venta_id}.pdf'
    
    return response

if __name__ == '__main__':
    from modelo.database import crear_base_datos
    crear_base_datos()  # Asegurar que la BD existe con las tablas necesarias
    app.run(debug=True, host='127.0.0.1', port=5000)