import re

# Leer el intérprete
s = open('nexuslang_v11.py', encoding='utf-8').read()

# Buscar la sección de tokens y agregar % si falta
if "'%'" not in s and '"%"' not in s:
    # Agregar % a los operadores
    s = s.replace("tokens = {", "tokens = {\n    '%': 'OP',")
    print("✅ Agregado operador %")
else:
    print("ℹ️ Operador % ya existe")

# Verificar si hay soporte para clases
if 'کلاس' in s and 'نیا' in s:
    print("✅ Clases ya implementadas")
else:
    print("⚠️ Clases no implementadas completamente")

# Guardar
open('nexuslang_v11.py', 'w', encoding='utf-8').write(s)
print("Guardado")
