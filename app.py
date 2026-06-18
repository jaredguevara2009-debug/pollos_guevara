from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
import mysql.connector
import hashlib
import os
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

print("🐔 Pollos Guevara iniciando...")

# ============================================================
# CONFIGURACIÓN PARA SUBIR IMÁGENES
# ============================================================
UPLOAD_FOLDER = 'static/img/productos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ============================================================
# FUNCIONES DE BASE DE DATOS
# ============================================================
def get_connection():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE,
        port=Config.MYSQL_PORT
    )

def hash_password(password):
    return password

# ============================================================
# LOGIN
# ============================================================
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    correo = request.form['correo']
    password = hash_password(request.form['password'])
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE correo = %s AND password = %s", (correo, password))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if usuario:
        session['user_id'] = usuario['id']
        session['user_correo'] = usuario['correo']
        session['user_rol'] = usuario['rol']
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error="Correo o contraseña incorrectos")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ============================================================
# DASHBOARD
# ============================================================
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html')

# ============================================================
# CRUD USUARIOS
# ============================================================
@app.route('/usuarios')
def listar_usuarios():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios ORDER BY id DESC")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuarios/nuevo', methods=['GET', 'POST'])
def nuevo_usuario():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        password = hash_password(request.form['password'])
        rol = request.form['rol']
        
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuarios (nombre, correo, password, rol) VALUES (%s, %s, %s, %s)",
                (nombre, correo, password, rol)
            )
            conn.commit()
            flash('✅ Usuario creado correctamente', 'success')
        except mysql.connector.IntegrityError:
            flash('❌ El correo ya está registrado', 'danger')
        except Exception as e:
            flash(f'❌ Error: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('listar_usuarios'))
    return render_template('usuario_form.html', usuario=None)

@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        rol = request.form['rol']
        password = request.form.get('password', '')
        
        try:
            if password:
                password = hash_password(password)
                cursor.execute(
                    "UPDATE usuarios SET nombre=%s, correo=%s, password=%s, rol=%s WHERE id=%s",
                    (nombre, correo, password, rol, id)
                )
            else:
                cursor.execute(
                    "UPDATE usuarios SET nombre=%s, correo=%s, rol=%s WHERE id=%s",
                    (nombre, correo, rol, id)
                )
            conn.commit()
            flash('✅ Usuario actualizado correctamente', 'success')
        except mysql.connector.IntegrityError:
            flash('❌ El correo ya está registrado', 'danger')
        except Exception as e:
            flash(f'❌ Error: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('listar_usuarios'))
    
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('usuario_form.html', usuario=usuario)

@app.route('/usuarios/eliminar/<int:id>')
def eliminar_usuario(id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('✅ Usuario eliminado correctamente', 'success')
    return redirect(url_for('listar_usuarios'))

# ============================================================
# CRUD PRODUCTOS
# ============================================================
@app.route('/productos')
def listar_productos():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos ORDER BY id DESC")
        productos = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('productos.html', productos=productos, busqueda=None)
    except Exception as e:
        print(f"❌ Error en listar_productos: {e}")
        flash('❌ Error al cargar los productos', 'danger')
        return render_template('productos.html', productos=[], busqueda=None)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']
        categoria = request.form.get('categoria', 'pollos')
        imagen = ''
        
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_name = f"{int(time.time())}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_name))
                imagen = f"/static/img/productos/{unique_name}"
        
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO productos (nombre, precio, stock, categoria, imagen) 
                VALUES (%s, %s, %s, %s, %s)
            """, (nombre, precio, stock, categoria, imagen))
            conn.commit()
            flash('✅ Producto creado correctamente', 'success')
        except Exception as e:
            flash(f'❌ Error: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('listar_productos'))
    
    return render_template('producto_form.html', producto=None)

@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']
        categoria = request.form.get('categoria', 'pollos')
        imagen = request.form.get('imagen_actual', '')
        
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_name = f"{int(time.time())}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_name))
                imagen = f"/static/img/productos/{unique_name}"
        
        try:
            cursor.execute("""
                UPDATE productos 
                SET nombre=%s, precio=%s, stock=%s, categoria=%s, imagen=%s 
                WHERE id=%s
            """, (nombre, precio, stock, categoria, imagen, id))
            conn.commit()
            flash('✅ Producto actualizado correctamente', 'success')
        except Exception as e:
            flash(f'❌ Error: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('listar_productos'))
    
    cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('producto_form.html', producto=producto)

@app.route('/productos/eliminar/<int:id>')
def eliminar_producto(id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('✅ Producto eliminado correctamente', 'success')
    return redirect(url_for('listar_productos'))

# ============================================================
# BUSCADOR DE PRODUCTOS (BUSCA TODOS CON "P")
# ============================================================
@app.route('/productos/buscar')
def buscar_productos():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    busqueda = request.args.get('q', '').strip()
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Buscar productos que contengan el texto (insensible a mayúsculas)
        cursor.execute(
            "SELECT * FROM productos WHERE LOWER(nombre) LIKE LOWER(%s) OR LOWER(nombre) LIKE LOWER(%s)",
            (f'%{busqueda}%', f'%{busqueda}%')
        )
        productos = cursor.fetchall()
    except Exception as e:
        print(f"❌ Error en buscar: {e}")
        productos = []
    finally:
        cursor.close()
        conn.close()
    
    return render_template('productos.html', productos=productos, busqueda=busqueda)

# ============================================================
# VENTAS
# ============================================================
@app.route('/ventas', methods=['GET', 'POST'])
def ventas():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        producto_id = request.form['producto_id']
        cantidad = int(request.form['cantidad'])
        
        cursor.execute("SELECT * FROM productos WHERE id = %s", (producto_id,))
        producto = cursor.fetchone()
        
        if producto and producto['stock'] >= cantidad:
            total = producto['precio'] * cantidad
            
            cursor.execute(
                "INSERT INTO ventas (producto_id, cantidad, total) VALUES (%s, %s, %s)",
                (producto_id, cantidad, total)
            )
            
            nuevo_stock = producto['stock'] - cantidad
            cursor.execute("UPDATE productos SET stock = %s WHERE id = %s", (nuevo_stock, producto_id))
            
            conn.commit()
            flash(f'✅ Venta registrada: {producto["nombre"]} x {cantidad} = Bs {total}', 'success')
        else:
            flash('❌ Stock insuficiente o producto no encontrado', 'danger')
        
        cursor.close()
        conn.close()
        return redirect(url_for('ventas'))
    
    cursor.execute("SELECT * FROM productos WHERE stock > 0 ORDER BY nombre")
    productos = cursor.fetchall()
    
    cursor.execute("""
        SELECT v.*, p.nombre as producto_nombre 
        FROM ventas v 
        JOIN productos p ON v.producto_id = p.id 
        ORDER BY v.fecha DESC LIMIT 20
    """)
    ventas = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('ventas.html', productos=productos, ventas=ventas)

# ============================================================
# EJECUCIÓN
# ============================================================
if __name__ == '__main__':
    print("🚀 Servidor en http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)