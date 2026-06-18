import mysql.connector

# Tus credenciales de Clever Cloud
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
    print("✅ Columna 'categoria' agregada correctamente")
except Exception as e:
    print(f"⚠️ La columna ya existe o error: {e}")

# Actualizar categorías
categorias = {
    1: 'pollos', 2: 'pollos', 3: 'pollos', 4: 'pollos', 5: 'pollos',
    6: 'pollos', 7: 'pollos', 8: 'pollos', 9: 'pollos', 10: 'pollos',
    11: 'pollos', 12: 'pollos', 13: 'pollos',
    14: 'combos', 15: 'combos', 16: 'combos', 17: 'combos', 18: 'combos',
    19: 'combos', 20: 'combos', 21: 'combos',
    22: 'papas', 23: 'papas', 24: 'papas', 25: 'papas', 26: 'papas',
    27: 'papas', 28: 'papas', 29: 'papas', 30: 'papas', 31: 'papas',
    32: 'papas', 33: 'papas', 34: 'papas', 35: 'papas', 36: 'papas',
    37: 'refrescos', 38: 'refrescos', 39: 'refrescos', 40: 'refrescos',
    41: 'refrescos', 42: 'refrescos', 43: 'refrescos', 44: 'refrescos',
    45: 'refrescos', 46: 'refrescos', 47: 'refrescos', 48: 'refrescos',
    49: 'refrescos', 50: 'refrescos', 51: 'refrescos', 52: 'refrescos',
    53: 'refrescos',
    54: 'postres', 55: 'postres', 56: 'postres', 57: 'postres',
    58: 'salsas', 59: 'salsas', 60: 'salsas', 61: 'salsas',
    62: 'extras', 63: 'extras'
}

for id_prod, categoria in categorias.items():
    cursor.execute("UPDATE productos SET categoria = %s WHERE id = %s", (categoria, id_prod))

conn.commit()
cursor.close()
conn.close()

print("✅ Categorías actualizadas correctamente")
print("🎉 ¡Listo! Ahora puedes ver los productos organizados por categorías")