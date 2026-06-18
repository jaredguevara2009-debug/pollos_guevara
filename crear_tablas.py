import mysql.connector

# Tus credenciales de Clever Cloud
config = {
    'host': 'bkyu0pg3kyj6hv6ei5f-mysql.services.clever-cloud.com',
    'user': 'uesdjuurlsg5fqu2',
    'password': 'Ky5ALiNzj4BWYGiJwp2h',
    'database': 'bkyu0pg3kyj6hv6ei5f'
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    print("✅ Conectado a Clever Cloud")

    # Crear tabla usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            correo VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            rol VARCHAR(50) DEFAULT 'vendedor'
        )
    ''')
    print("✅ Tabla 'usuarios' creada")

    # Crear tabla productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            precio DECIMAL(10,2) NOT NULL,
            stock INT NOT NULL,
            imagen VARCHAR(255)
        )
    ''')
    print("✅ Tabla 'productos' creada")

    # Crear tabla ventas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            producto_id INT,
            cantidad INT NOT NULL,
            total DECIMAL(10,2) NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    ''')
    print("✅ Tabla 'ventas' creada")

    conn.commit()
    cursor.close()
    conn.close()
    print("🎉 ¡Todas las tablas creadas con éxito!")

except mysql.connector.Error as err:
    print(f"❌ Error: {err}")