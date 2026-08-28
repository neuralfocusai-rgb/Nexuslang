import re

with open('nexuslang.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Actualizar versión
code = code.replace('VERSION = "5.2.0"', 'VERSION = "5.3.0"')

# 2. Agregar keywords async/await y tipos
old_keywords = """KEYWORDS = [
    (r'\\bsino\\b', 'else'), (r'\\bsi\\b', 'if'), (r'\\bmientras\\b', 'while'),
    (r'\\bpara\\b', 'for'), (r'\\ben\\b', 'in'), (r'\\bdevolver\\b', 'return'),
    (r'\\bfuncion\\b', 'def'), (r'\\bclase\\b', 'class'), (r'\\bromper\\b', 'break'),
    (r'\\bcontinuar\\b', 'continue'), (r'\\bintentar\\b', 'try'), (r'\\beste\\b', 'self'),
    (r'\\bno\\b', 'not'), (r'\\bverdadero\\b', 'True'), (r'\\bfalso\\b', 'False'),
    (r'\\bnulo\\b', 'None'), (r'\\bimprimir\\b', 'print'), (r'\\bmostrar\\b', 'print'),
    (r'&&', ' and '), (r'\\|\\|', ' or '),
]"""

new_keywords = """KEYWORDS = [
    (r'\\bsino\\b', 'else'), (r'\\bsi\\b', 'if'), (r'\\bmientras\\b', 'while'),
    (r'\\bpara\\b', 'for'), (r'\\ben\\b', 'in'), (r'\\bdevolver\\b', 'return'),
    (r'\\bfuncion\\b', 'def'), (r'\\bclase\\b', 'class'), (r'\\bromper\\b', 'break'),
    (r'\\bcontinuar\\b', 'continue'), (r'\\bintentar\\b', 'try'), (r'\\bfinalmente\\b', 'finally'),
    (r'\\bcapturar\\b', 'except'), (r'\\beste\\b', 'self'), (r'\\basincrono\\b', 'async'),
    (r'\\basync\\b', 'async'), (r'\\besperar\\b', 'await'), (r'\\bawait\\b', 'await'),
    (r'\\bno\\b', 'not'), (r'\\bverdadero\\b', 'True'), (r'\\bfalso\\b', 'False'),
    (r'\\bnulo\\b', 'None'), (r'\\bimprimir\\b', 'print'), (r'\\bmostrar\\b', 'print'),
    (r'&&', ' and '), (r'\\|\\|', ' or '),
]"""

code = code.replace(old_keywords, new_keywords)

# 3. Agregar función para remover tipos opcionales (los ignoramos en runtime)
code = code.replace(
    "def _fix_linea(self, s):",
    """def _strip_types(self, s):
        # Remove type hints: def sumar(a: int, b: int) -> int => a + b
        # Becomes: def sumar(a, b) => a + b
        s = re.sub(r':\\s*(int|str|float|bool|list|dict|None|Any)\\b', '', s)
        s = re.sub(r'->\\s*(int|str|float|bool|list|dict|None|Any)\\b', '', s)
        return s
    
    def _fix_linea(self, s):"""
)

# 4. Actualizar _fix_linea para usar _strip_types
code = code.replace(
    "def _fix_linea(self, s):\n        m = re.match(r'^def\\s+(\\w+)\\s*\\(([^)]*)\\)\\s*=>\\s*(.+)$', s)",
    """def _fix_linea(self, s):
        s = self._strip_types(s)
        m = re.match(r'^def\\s+(\\w+)\\s*\\(([^)]*)\\)\\s*=>\\s*(.+)$', s)"""
)

# 5. Agregar manejo de errores mejorado con contexto
old_ejecutar = """    def ejecutar(self, codigo):
        self.output = []
        py = self.transpilar(codigo)
        try:
            exec(compile(py, 'nexuslang', 'exec'), self.ns)
        except Exception as e:
            tb = sys.exc_info()[2]
            lineno = None
            while tb:
                if tb.tb_frame.f_code.co_name == '<module>':
                    lineno = tb.tb_lineno
                tb = tb.tb_next
            self.out(f"Error{' en linea ' + str(lineno) if lineno else ''}: {e}")
        return {'output': self.output, 'db': self.ns['db']._data}"""

new_ejecutar = """    def ejecutar(self, codigo):
        self.output = []
        py = self.transpilar(codigo)
        lineas_py = py.split('\\n')
        try:
            exec(compile(py, 'nexuslang', 'exec'), self.ns)
        except Exception as e:
            tb = sys.exc_info()[2]
            lineno = None
            while tb:
                if tb.tb_frame.f_code.co_name == '<module>':
                    lineno = tb.tb_lineno
                tb = tb.tb_next
            
            error_msg = f"❌ Error{' en linea ' + str(lineno) if lineno else ''}: {type(e).__name__}: {e}"
            
            if lineno and lineno <= len(lineas_py):
                context_start = max(1, lineno - 2)
                context_end = min(len(lineas_py), lineno + 1)
                for i in range(context_start, context_end + 1):
                    prefix = "→" if i == lineno else " "
                    error_msg += f"\\n   {prefix} {i:3d} │ {lineas_py[i-1]}"
                if lineno <= len(lineas_py):
                    error_msg += f"\\n     {' ' * len(lineas_py[lineno-1])} ^ {e}"
            
            self.out(error_msg)
        return {'output': self.output, 'db': self.ns['db']._data}"""

code = code.replace(old_ejecutar, new_ejecutar)

# 6. Agregar funciones async de ejemplo
old_web_class = """        class Web:
            @staticmethod
            def obtener(url, timeout=10):
                with urlreq.urlopen(url, timeout=timeout) as r:
                    return r.read().decode('utf-8')
            get = obtener"""

new_web_class = """        class Web:
            @staticmethod
            def obtener(url, timeout=10):
                with urlreq.urlopen(url, timeout=timeout) as r:
                    return r.read().decode('utf-8')
            get = obtener
            @staticmethod
            async def obtener_async(url, timeout=10):
                import asyncio
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(None, lambda: Web.obtener(url, timeout))
            get_async = obtener_async"""

code = code.replace(old_web_class, new_web_class)

# 7. Agregar asyncio al namespace
code = code.replace(
    "ns['print'] = self._print",
    """import asyncio
        ns['asyncio'] = asyncio
        ns['async_run'] = asyncio.run
        ns['print'] = self._print"""
)

# 8. Agregar tests 20-23
old_tests = """    check("19. Web server (APIs)", hasattr(NexusLang(mostrar=False).ns['web'], 'servidor'))
    check("20. Full-stack HTML+JSON", es_html("<html>x</html>") and not es_html({"a": 1}))"""

new_tests = """    check("19. Web server (APIs)", hasattr(NexusLang(mostrar=False).ns['web'], 'servidor'))
    check("20. Full-stack HTML+JSON", es_html("<html>x</html>") and not es_html({"a": 1}))
    
    l = NexusLang(mostrar=False)
    l.ejecutar('def sumar(a: int, b: int) -> int => a + b\\nimprimir(sumar(5, 3))')
    check("21. Type hints", '8' in l.output, str(l.output))
    
    l = NexusLang(mostrar=False)
    l.ejecutar('async funcion async_test():\\n    devolver "async works"\\nresultado = async_run(async_test())\\nimprimir(resultado)')
    check("22. Async/await", 'async works' in l.output, str(l.output))
    
    l = NexusLang(mostrar=False)
    l.ejecutar('imprimir(x_inexistente)')
    has_context = '│' in l.output[0] if l.output else False
    check("23. Error context", has_context, str(l.output))"""

code = code.replace(old_tests, new_tests)
code = code.replace("(20 tests)", "(23 tests)")

# 9. Agregar ejemplo de demo profesional
with open('examples/demo_profesional.nx', 'w', encoding='utf-8') as f:
    f.write("""// NexusLang v5.3 - DEMO PROFESIONAL
// Async + Tipos + IA + Full-stack + Manejo de errores

// 1. Función con tipos
def calcular_total(precio: float, cantidad: int) -> float => precio * cantidad

// 2. Clase con tipos
clase Producto:
    def __init__(nombre: str, precio: float):
        este.nombre = nombre
        este.precio = precio
    
    def info() -> str:
        devolver f"{este.nombre}: ${este.precio}"

// 3. Async function
async funcion obtener_api():
    data = esperar web.obtener_async("http://httpbin.org/json")
    devolver json_parsear(data)

// 4. Manejo de errores con contexto
intentar:
    resultado = calcular_total(100.5, 3)
    imprimir("Total: $" + texto(resultado))
    
    p = Producto("Laptop Pro", 999.99)
    imprimir(p.info())
    
    api_data = async_run(obtener_api())
    imprimir("API: " + texto(api_data))
    
capturar (error):
    imprimir("Error capturado: " + texto(error))

// 5. IA integrada
texto_review = "Este producto es excelente y muy fácil de usar"
sentimiento = ia.sentimiento(texto_review)
imprimir("Sentimiento: " + texto(sentimiento))

// 6. Base de datos
db.productos.laptop = {"nombre": "Laptop", "precio": 999}
imprimir("DB: " + texto(db.productos.laptop))

imprimir("✅ Demo completado - NexusLang v5.3 Professional")
""")

with open('nexuslang.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ UPGRADE TO v5.3.0 COMPLETE")
print("   - Async/await agregado")
print("   - Type hints opcionales")
print("   - Errores con contexto visual")
print("   - Demo profesional creado")
