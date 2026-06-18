import mysql.connector
import time

print("🔧 Arreglando categorías...")

# Conectar a la base de datos
conn = mysql.connector.connect(
    host='bkyu0pg3kyj6hv6eic5f-mysql.services.clever-cloud.com',
    user='uesdjuurlsg5fqu2',
    password='Ky5ALiNzj4BWYGiJwp2h',
    database='bkyu0pg3kyj6hv6eic5f'
)

cursor = conn.cursor()

# 1. Verificar si la columna existe
cursor.execute("SHOW COLUMNS FROM productos LIKE 'categoria'")
existe = cursor.fetchone()

if not existe:
    print("📌 Columna 'categoria' NO existe. Creando...")
    cursor.execute("ALTER TABLE productos ADD COLUMN categoria VARCHAR(50) DEFAULT 'pollos'")
    conn.commit()
    print("✅ Columna 'categoria' creada")
else:
    print("✅ Columna 'categoria' ya existe")

# 2. Asignar categorías a productos existentes
cursor.execute("UPDATE productos SET categoria = 'pollos' WHERE categoria IS NULL OR categoria = ''")
conn.commit()
print("✅ Categorías asignadas a productos")

# 3. Verificar productos
cursor.execute("SELECT COUNT(*) FROM productos")
count = cursor.fetchone()[0]
print(f"📦 Total de productos: {count}")

# 4. Mostrar algunos productos
cursor.execute("SELECT id, nombre, categoria FROM productos LIMIT 5")
productos = cursor.fetchall()
print("📋 Primeros 5 productos:")
for p in productos:
    print(f"  - {p[0]}: {p[1]} → {p[2]}")

cursor.close()
conn.close()
print("🎉 ¡ARREGLO COMPLETADO!")