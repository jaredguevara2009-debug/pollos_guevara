import mysql.connector

# Tus datos de Clever Cloud
conn = mysql.connector.connect(
    host='bkyu0pg3kyj6hv6eic5f-mysql.services.clever-cloud.com',
    user='uesdjuurlsg5fqu2',
    password='Ky5ALiNzj4BWYGiJwp2h',
    database='bkyu0pg3kyj6hv6eic5f'
)

cursor = conn.cursor()

# Agregar columna categoria
try:
    cursor.execute("ALTER TABLE productos ADD COLUMN categoria VARCHAR(50) DEFAULT 'pollos'")
    print("✅ Columna 'categoria' agregada")
except Exception as e:
    print(f"⚠️ {e}")

# Actualizar productos existentes
cursor.execute("UPDATE productos SET categoria = 'pollos' WHERE categoria IS NULL OR categoria = ''")
conn.commit()
cursor.close()
conn.close()

print("✅ ¡Listo! Productos actualizados.")