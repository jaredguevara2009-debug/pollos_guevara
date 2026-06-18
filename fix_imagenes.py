import mysql.connector

conn = mysql.connector.connect(
    host='bkyu0pg3kyj6hv6eic5f-mysql.services.clever-cloud.com',
    user='uesdjuurlsg5fqu2',
    password='Ky5ALiNzj4BWYGiJwp2h',
    database='bkyu0pg3kyj6hv6eic5f'
)

cursor = conn.cursor()

# Actualizar imágenes
cursor.execute("UPDATE productos SET imagen = 'https://cdn-icons-png.flaticon.com/512/3050/3050204.png' WHERE categoria = 'pollos'")
cursor.execute("UPDATE productos SET imagen = 'https://cdn-icons-png.flaticon.com/512/3050/3050204.png' WHERE categoria = 'combos'")
cursor.execute("UPDATE productos SET imagen = 'https://cdn-icons-png.flaticon.com/512/3050/3050204.png' WHERE categoria = 'papas'")
cursor.execute("UPDATE productos SET imagen = 'https://cdn-icons-png.flaticon.com/512/3050/3050204.png' WHERE categoria = 'refrescos'")
cursor.execute("UPDATE productos SET imagen = 'https://cdn-icons-png.flaticon.com/512/3050/3050204.png' WHERE categoria = 'postres'")
cursor.execute("UPDATE productos SET imagen = 'https://cdn-icons-png.flaticon.com/512/3050/3050204.png' WHERE categoria = 'salsas'")
cursor.execute("UPDATE productos SET imagen = 'https://cdn-icons-png.flaticon.com/512/3050/3050204.png' WHERE categoria = 'extras'")

conn.commit()
cursor.close()
conn.close()

print("✅ Imágenes actualizadas con URLs externas")