from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'clave_secreta'

def iniciar_sesion():
    if 'productos' not in session:
        session['productos'] = []

@app.route('/')
def index():
    iniciar_sesion()
    return render_template('index.html', productos=session['productos'])

@app.route('/agregar', methods=['POST'])
def agregar_producto():
    iniciar_sesion()
    productos = session['productos']
    nombre = request.form['nombre']
    cantidad = int(request.form['cantidad'])
    precio = float(request.form['precio'])
    fecha_vencimiento = request.form['fecha_vencimiento']
    categoria = request.form['categoria']
    id_producto = len(productos) + 1  

    producto = {
        'id': id_producto,
        'nombre': nombre,
        'cantidad': cantidad,
        'precio': precio,
        'fecha_vencimiento': fecha_vencimiento,
        'categoria': categoria
    }
    productos.append(producto)
    session['productos'] = productos
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
def eliminar_producto(id):
    iniciar_sesion()
    session['productos'] = [p for p in session['productos'] if p['id'] != id]
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    iniciar_sesion()
    producto = next((p for p in session['productos'] if p['id'] == id), None)
    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']
        session.modified = True
        return redirect(url_for('index'))
    return render_template('editar.html', producto=producto)

if __name__ == '__main__':
    app.run(debug=True)

