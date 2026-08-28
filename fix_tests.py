import re

with open('nexuslang.py', 'r') as f:
    content = f.read()

# Reemplazar la función pruebas completa
old_tests = """def pruebas():
    print("="*70)
    print(f"NEXUSLANG v{VERSION} - PRUEBAS COMPLETAS")
    print("="*70)
    
    lang = NexusLang()
    
    lang.ejecutar('''
# 1. Variables
nombre = "Lucas"
edad = 25
imprimir "Hola " + nombre + ", tienes " + texto(edad) + " anos"

# 2. Matematicas
imprimir "Pi: " + texto(mate.pi)
imprimir "Raiz de 144: " + texto(mate.raiz(144))
imprimir "2^10: " + texto(mate.potencia(2, 10))

# 3. IA
texto_prueba = "Me encanta NexusLang, es excelente y poderoso"
imprimir "Sentimiento: " + texto(ia.sentimiento(texto_prueba))
imprimir "Chatbot: " + ia.chatbot("hola como estas")
imprimir "Palabras clave: " + texto(ia.palabras_clave(texto_prueba, 3))

# 4. Web
html = web.pagina("Mi Web", web.parrafo("Creado con NexusLang v3.0") + web.boton("Click"))
imprimir web.guardar("demo", html)

# 5. Archivos
archivo_escribir("prueba.txt", "NexusLang es el mejor lenguaje")
contenido = archivo_leer("prueba.txt")
imprimir "Archivo leido: " + contenido

# 6. Base de datos
db.usuarios.lucas = {"nombre": "Lucas", "edad": 25, "skills": ["Python", "JS"]}
db.usuarios.ana = {"nombre": "Ana", "edad": 30}
imprimir "Usuario Lucas: " + texto(db.usuarios.lucas.get())

# 7. Listas
numeros = [5, 2, 9, 1, 7]
imprimir "Ordenados: " + texto(ordenar(numeros))
imprimir "Maximo: " + texto(max(numeros))

# 8. Tiempo
imprimir "Hora actual: " + hora_actual()
''')"""

new_tests = """def pruebas():
    print("="*70)
    print(f"NEXUSLANG v{VERSION} - PRUEBAS COMPLETAS")
    print("="*70)
    
    lang = NexusLang()
    
    lang.ejecutar('''
# 1. Variables
nombre = "Lucas"
edad = 25
imprimir("Hola " + nombre + ", tienes " + texto(edad) + " anos")

# 2. Matematicas
imprimir("Pi: " + texto(mate.pi))
imprimir("Raiz de 144: " + texto(mate.raiz(144)))
imprimir("2^10: " + texto(mate.potencia(2, 10)))

# 3. IA
texto_prueba = "Me encanta NexusLang, es excelente y poderoso"
imprimir("Sentimiento: " + texto(ia.sentimiento(texto_prueba)))
imprimir("Chatbot: " + ia.chatbot("hola como estas"))
imprimir("Palabras clave: " + texto(ia.palabras_clave(texto_prueba, 3)))

# 4. Web
html = web.pagina("Mi Web", web.parrafo("Creado con NexusLang v3.0") + web.boton("Click"))
imprimir(web.guardar("demo", html))

# 5. Archivos
archivo_escribir("prueba.txt", "NexusLang es el mejor lenguaje")
contenido = archivo_leer("prueba.txt")
imprimir("Archivo leido: " + contenido)

# 6. Base de datos
db.usuarios.lucas = {"nombre": "Lucas", "edad": 25, "skills": ["Python", "JS"]}
db.usuarios.ana = {"nombre": "Ana", "edad": 30}
imprimir("Usuario Lucas: " + texto(db.usuarios.lucas.get()))

# 7. Listas
numeros = [5, 2, 9, 1, 7]
imprimir("Ordenados: " + texto(ordenar(numeros)))
imprimir("Maximo: " + texto(max(numeros)))

# 8. Tiempo
imprimir("Hora actual: " + hora_actual())
''')"""

content = content.replace(old_tests, new_tests)

with open('nexuslang.py', 'w') as f:
    f.write(content)

print("✅ Código corregido!")
