from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
import sys

app = Flask(__name__)
app.secret_key = "pollos_guevara_secret"

print("🐔 Pollos Guevara iniciando...", flush=True)
sys.stdout.flush()

USUARIO_ADMIN = {
    'correo': 'admin@pollos.com',
    'password': hashlib.sha256('admin123'.encode()).hexdigest(),
    'rol': 'admin'
}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    print("📄 Mostrando login", flush=True)
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    correo = request.form['correo']
    password = hash_password(request.form['password'])
    
    print(f"🔐 Intentando login: {correo}", flush=True)
    
    if correo == USUARIO_ADMIN['correo'] and password == USUARIO_ADMIN['password']:
        session['user_id'] = 1
        session['user_correo'] = correo
        session['user_rol'] = 'admin'
        print("✅ Login exitoso", flush=True)
        return redirect(url_for('dashboard'))
    else:
        print("❌ Login fallido", flush=True)
        return render_template('login.html', error="Correo o contraseña incorrectos")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html')

if __name__ == '__main__':
    print("🚀 Servidor en http://127.0.0.1:5000", flush=True)
    app.run(debug=True, host='0.0.0.0', port=5000)