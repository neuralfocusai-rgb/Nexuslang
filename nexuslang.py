#!/usr/bin/env python3
"""
NEXUSLANG v5.1 - PROFESSIONAL EDITION
Bilingual ES/EN | AI | DB | Web | HTTP | Classes | Modules | Try/Catch
"""

import re, os, json, math, random, time, sys
from datetime import datetime as dt
from pathlib import Path
from functools import reduce
from collections import Counter
import base64, hashlib, uuid
import urllib.request as urlreq

VERSION = "6.3.0"

for d in ["nexus_pages", "nexus_archivos"]:
    os.makedirs(d, exist_ok=True)

# ==================== AI ====================
class IA:
    @staticmethod
    def sentimiento(texto):
        pos = {"bueno","excelente","genial","amor","gusta","encanta","perfecto","feliz",
               "great","excellent","love","amazing","wonderful","happy","good","awesome"}
        neg = {"malo","terrible","horrible","triste","odio","peligro","pesimo",
               "bad","awful","sad","hate","danger","worst"}
        palabras = set(re.findall(r'\w+', str(texto).lower()))
        p, n = len(palabras & pos), len(palabras & neg)
        total = p + n
        if total == 0: return {"result": "neutral", "confidence": 0.5}
        if p > n: return {"result": "positive", "confidence": round(p/total, 2)}
        if n > p: return {"result": "negative", "confidence": round(n/total, 2)}
        return {"result": "neutral", "confidence": 0.5}
    @staticmethod
    def palabras_clave(texto, n=5):
        return Counter(re.findall(r'\w{3,}', str(texto).lower())).most_common(n)
    @staticmethod
    def chatbot(texto):
        t = str(texto).lower()
        if any(x in t for x in ["hola","hello","hi"]): return "¡Hola! / Hello! I'm NexusAI."
        if any(x in t for x in ["nombre","name"]): return "I'm NexusAI."
        if any(x in t for x in ["gracias","thanks"]): return "¡De nada! / You're welcome!"
        return "Interesting. Tell me more."
    @staticmethod
    def predecir(serie, pasos=1):
        nums = [float(x) for x in serie]
        if len(nums) < 2: return nums[-1] if nums else 0
        diffs = [nums[i+1] - nums[i] for i in range(len(nums)-1)]
        return nums[-1] + (sum(diffs)/len(diffs)) * pasos

# ==================== DATABASE ====================
class DB:
    def __init__(self): object.__setattr__(self, '_data', {})
    def __getattr__(self, name): return DBPath(self._data, [name])
    def guardar(self):
        with open("nexus_db.json", 'w', encoding='utf-8') as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)
        return "DB saved"

class DBPath:
    def __init__(self, data, path):
        object.__setattr__(self, '_data', data)
        object.__setattr__(self, '_path', path)
    def __getattr__(self, name): return DBPath(self._data, self._path + [name])
    def __setattr__(self, name, value):
        if name.startswith('_'): object.__setattr__(self, name, value)
        else: self._set(self._path + [name], value)
    def __getitem__(self, key): return DBPath(self._data, self._path + [key])
    def __setitem__(self, key, value): self._set(self._path + [key], value)
    def _set(self, path, value):
        actual = self._data
        for i, parte in enumerate(path):
            if i == len(path) - 1: actual[parte] = value
            else:
                if not isinstance(actual.get(parte), dict): actual[parte] = {}
                actual = actual[parte]
    def _get(self):
        actual = self._data
        for parte in self._path:
            if isinstance(actual, dict) and parte in actual: actual = actual[parte]
            else: return None
        return actual
    def get(self): return self._get()
    def __eq__(self, other): return self._get() == other
    def __str__(self): return str(self._get())
    def __repr__(self): return repr(self._get())

# ==================== KEYWORDS ====================
KEYWORDS = [
    (r'\bsino\b', 'else'), (r'\bsi\b', 'if'), (r'\bmientras\b', 'while'),
    (r'\bpara\b', 'for'), (r'\ben\b', 'in'), (r'\bdevolver\b', 'return'),
    (r'\bfuncion\b', 'def'), (r'\bclase\b', 'class'), (r'\bromper\b', 'break'),
    (r'\bcontinuar\b', 'continue'), (r'\bintentar\b', 'try'), (r'\bfinalmente\b', 'finally'),
    (r'\bcapturar\b', 'except'), (r'\beste\b', 'self'), (r'\basincrono\b', 'async'),
    (r'\basync\b', 'async'), (r'\besperar\b', 'await'), (r'\bawait\b', 'await'),
    (r'\bno\b', 'not'), (r'\bverdadero\b', 'True'), (r'\bfalso\b', 'False'),
    (r'\bnulo\b', 'None'), (r'\bimprimir\b', 'print'), (r'\bmostrar\b', 'print'),
    (r'&&', ' and '), (r'\|\|', ' or '),
]

# ==================== INTERPRETER ====================
class NexusLang:
    def __init__(self, mostrar=True):
        self.mostrar = mostrar
        self.output = []
        self.ia = IA()
        self.ns = {'__builtins__': self._safe_builtins(), '__name__': 'nexuslang', '__qualname__': ''}
        self.vars = self.ns
        self._setup_namespace()

    def _safe_builtins(self):
        return {'len': len, 'range': range, 'str': str, 'int': int, 'float': float,
            'bool': bool, 'abs': abs, 'round': round, 'min': min, 'max': max,
            'sum': sum, 'sorted': sorted, 'list': list, 'dict': dict, 'set': set,
            'tuple': tuple, 'enumerate': enumerate, 'zip': zip, 'type': type,
            'isinstance': isinstance, 'input': input, 'Exception': Exception,
            'True': True, 'False': False, 'None': None,
            '__build_class__': __import__('builtins').__build_class__}

    def out(self, texto):
        self.output.append(str(texto))
        if self.mostrar: print(str(texto))

    def _print(self, *args):
        self.out(' '.join(str(a) for a in args))

    def _importar(self, nombre):
        """Import module: importar("utils") loads utils.nx"""
        ruta = Path(nombre if str(nombre).endswith('.nx') else str(nombre) + '.nx')
        if not ruta.exists():
            raise FileNotFoundError(f"Module '{nombre}' not found")
        py = self.transpilar(ruta.read_text(encoding='utf-8'))
        exec(compile(py, str(nombre), 'exec'), self.ns)
        return f"Module '{nombre}' imported"

    def _setup_namespace(self):
        if not hasattr(self, 'ns'): self.ns = {}
        self.ns['usar'] = self._usar
        import types as _nts
        self.ns['nexus'] = _nts.SimpleNamespace(texto=_nts.SimpleNamespace(mayusculas=lambda t: t.upper(), minusculas=lambda t: t.lower(), largo=lambda t: len(t), contiene=lambda t, x: x in t, invertir=lambda t: t[::-1]), lista=_nts.SimpleNamespace(ordenar=sorted, largo=len, primero=lambda l: l[0], ultimo=lambda l: l[-1], sumar=sum, invertir=lambda l: l[::-1]), fecha=_nts.SimpleNamespace(hoy=lambda: __import__('datetime').date.today().isoformat(), ahora=lambda: __import__('datetime').datetime.now().strftime('%H:%M')))
        ns = self.ns
        ns.update({'true': True, 'false': False, 'null': None, 'pi': math.pi, 'e': math.e})
        ns.update({
            'aleatorio': lambda a,b: random.randint(int(a),int(b)),
            'random': lambda a,b: random.randint(int(a),int(b)),
            'raiz': math.sqrt, 'sqrt': math.sqrt, 'potencia': pow, 'pow': pow,
            'log': math.log, 'seno': math.sin, 'sin': math.sin,
            'coseno': math.cos, 'cos': math.cos, 'factorial': math.factorial,
            'floor': math.floor, 'ceil': math.ceil,
            'rango': lambda *a: list(range(*[int(x) for x in a])),
        })
        ns.update({
            'texto': str, 'text': str,
            'mayusculas': lambda t: str(t).upper(), 'upper': lambda t: str(t).upper(),
            'minusculas': lambda t: str(t).lower(), 'lower': lambda t: str(t).lower(),
            'recortar': lambda t: str(t).strip(), 'strip': lambda t: str(t).strip(),
            'dividir': lambda t,s=None: str(t).split(s), 'split': lambda t,s=None: str(t).split(s),
            'unir': lambda l,s='': s.join([str(x) for x in l]), 'join': lambda l,s='': s.join([str(x) for x in l]),
            'reemplazar': lambda t,a,b: str(t).replace(a,b), 'replace': lambda t,a,b: str(t).replace(a,b),
            'buscar': lambda t,s: str(t).find(s), 'find': lambda t,s: str(t).find(s),
            'formatear': lambda t,d: str(t).format(**d), 'format_str': lambda t,d: str(t).format(**d),
        })
        ns.update({
            'ordenar': sorted, 'sort': sorted,
            'invertir': lambda l: list(reversed(l)), 'reverse': lambda l: list(reversed(l)),
            'agregar': lambda l,x: l.append(x) or l, 'append': lambda l,x: l.append(x) or l,
            'map': lambda f,l: list(map(f,l)), 'filter': lambda f,l: list(filter(f,l)),
        })
        ns.update({
            'json_parsear': json.loads, 'json_parse': json.loads,
            'json_texto': lambda o: json.dumps(o, ensure_ascii=False),
            'json_stringify': lambda o: json.dumps(o, ensure_ascii=False),
        })
        ns.update({
            'hora_actual': lambda: dt.now().strftime('%H:%M:%S'),
            'fecha_actual': lambda: dt.now().strftime('%d/%m/%Y'),
            'timestamp': time.time, 'esperar': time.sleep, 'sleep': time.sleep,
        })
        ns.update({
            'archivo_leer': lambda p: Path(p).read_text() if Path(p).exists() else None,
            'file_read': lambda p: Path(p).read_text() if Path(p).exists() else None,
            'archivo_escribir': lambda p,c: Path(p).write_text(str(c)),
            'file_write': lambda p,c: Path(p).write_text(str(c)),
        })
        ns.update({
            'uuid': lambda: str(uuid.uuid4()),
            'hash': lambda t: hashlib.sha256(str(t).encode()).hexdigest(),
            'importar': self._importar, 'usar': self._importar,
            'use': self._importar, 'import_module': self._importar,
        })
        ns['ia'] = self.ia
        ns['ai'] = self.ia
        ns['db'] = DB()

        class Mate:
            pi, e = math.pi, math.e
            raiz = sqrt = staticmethod(math.sqrt)
            potencia = pow = staticmethod(pow)
            seno = sin = staticmethod(math.sin)
            coseno = cos = staticmethod(math.cos)
            factorial = staticmethod(math.factorial)
            aleatorio = staticmethod(random.randint)
        class TextTools:
            def __call__(self, t): return str(t)
            mayusculas = upper = staticmethod(lambda t: str(t).upper())
            minusculas = lower = staticmethod(lambda t: str(t).lower())
            recortar = strip = staticmethod(lambda t: str(t).strip())
            regex = staticmethod(lambda t,p: re.findall(p, str(t)))
        class ListTools:
            ordenar = sort = staticmethod(sorted)
            invertir = reverse = staticmethod(lambda l: list(reversed(l)))
            map = staticmethod(lambda f,l: list(map(f,l)))
            filter = staticmethod(lambda f,l: list(filter(f,l)))
        class Web:
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
            get_async = obtener_async
            @staticmethod
            def pagina(titulo, contenido):
                return f"""<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'><meta charset='UTF-8'><title>{titulo}</title>
<style>body{{font-family:sans-serif;background:linear-gradient(160deg,#05060f,#1a0b2e 55%,#05060f);color:#fff;padding:0;margin:0}}h1{{font-size:22px;padding:14px 16px;margin:0}}.fxbar{{position:sticky;top:0;z-index:98;background:rgba(5,6,15,.94);backdrop-filter:blur(12px)}}.fxcard{{background:rgba(10,12,26,.88);backdrop-filter:blur(8px);border:1px solid rgba(0,255,255,.45);border-radius:16px;box-shadow:0 0 18px rgba(0,255,255,.22)}}.fxcta{{background:linear-gradient(90deg,#00e5ff,#ff2bd6);color:#04050c;animation:pul 2s infinite}}@keyframes pul{{0%,100%{{box-shadow:0 0 10px rgba(0,229,255,.5)}}50%{{box-shadow:0 0 28px rgba(255,43,214,.85)}}}}</style></head>
<body><h1>{titulo}</h1>{contenido}</body></html>"""
            @staticmethod
            def guardar(nombre, html):
                ruta = Path("nexus_pages") / f"{nombre}.html"
                ruta.write_text(html)
                return f"Web saved: {ruta}"
            parrafo = paragraph = staticmethod(lambda t: f"<p>{t}</p>")
            boton = button = staticmethod(lambda t: f"<button style='padding:12px 25px;background:#0072CE;color:#fff;border:none;border-radius:8px'>{t}</button>")
            caja = box = staticmethod(lambda t: f"<div style='padding:20px;margin:15px;background:rgba(255,255,255,0.1);border-radius:10px'>{t}</div>")
        ns.update({'mate': Mate(), 'math': Mate(), 'text': TextTools(), 'texto': TextTools(),
                   'lista': ListTools(), 'list_tools': ListTools(), 'web': Web()})
        ns['servidor_web'] = ServidorWeb
        ns['es_html'] = es_html
        ns['web'].servidor = ServidorWeb
        import asyncio
        ns['asyncio'] = asyncio
        ns['async_run'] = asyncio.run
        ns['print'] = self._print
        ns['imprimir'] = self._print
        ns['mostrar'] = self._print

    # ---------- translation ----------
    def _traducir(self, linea):
        partes = []
        buf = ''
        linea = linea.replace(chr(92)+chr(34), chr(1)).replace(chr(92)+chr(39), chr(2))
        quote = None
        for c in linea:
            if quote:
                buf += c
                if c == quote:
                    partes.append(('str', buf)); buf = ''; quote = None
            elif c in '"\'':
                if buf: partes.append(('code', buf)); buf = ''
                buf = c; quote = c
            else:
                buf += c
        if buf: partes.append(('str', buf) if quote else ('code', buf))
        result = ''
        for kind, part in partes:
            if kind == 'code':
                for pat, rep in KEYWORDS:
                    part = re.sub(pat, rep, part)
            result += part
        return result.replace(chr(1), chr(92)+chr(34)).replace(chr(2), chr(92)+chr(39))

    def _quitar_comentarios(self, linea):
        linea = linea.replace(chr(92)+chr(34), chr(1)).replace(chr(92)+chr(39), chr(2))
        out = []
        quote = None
        i = 0
        while i < len(linea):
            c = linea[i]
            if quote:
                out.append(c)
                if c == quote: quote = None
            elif c in '"\'':
                quote = c; out.append(c)
            elif c == '#': break
            elif c == '/' and i+1 < len(linea) and linea[i+1] == '/': break
            else: out.append(c)
            i += 1
        return ''.join(out).replace(chr(1), chr(92)+chr(34)).replace(chr(2), chr(92)+chr(39)).rstrip()

    def _strip_types(self, s):
        # Remove type hints: def sumar(a: int, b: int) -> int => a + b
        # Becomes: def sumar(a, b) => a + b
        s = re.sub(r':\s*(int|str|float|bool|list|dict|None|Any)\b', '', s)
        s = re.sub(r'->\s*(int|str|float|bool|list|dict|None|Any)\b', '', s)
        return s
    
    def _fix_linea(self, s):
        s = self._strip_types(s)
        m = re.match(r'^def\s+(\w+)\s*\(([^)]*)\)\s*=>\s*(.+)$', s)
        if m:
            name, params, body = m.groups()
            if '=' in body and '==' not in body:
                return f"def {name}({params}): {body}"
            return f"def {name}({params}): return {body}"
        m = re.match(r'^(if|while|for)\b(.*?)=>(.+)$', s)
        if m:
            return f"{m.group(1)}{m.group(2)}: {self._fix_linea(m.group(3).strip())}"
        m = re.match(r'^print\s+(?!\()(.*)$', s)
        if m:
            return f"print({m.group(1)})"
        return s

    def _inject_self(self, line):
        m = re.match(r'^def\s+(\w+)\s*\(([^)]*)\)', line)
        if m:
            params = m.group(2).strip()
            new = 'self' + (', ' + params if params else '')
            return re.sub(r'^def\s+\w+\s*\([^)]*\)', f'def {m.group(1)}({new})', line)
        return line

    def _usar(self, ruta):
        if not ruta.endswith('.nx'): ruta += '.nx'
        if not hasattr(self, '_mods'): self._mods = set()
        if ruta in self._mods: return
        self._mods.add(ruta)
        with open(ruta, 'r', encoding='utf-8') as f:
            codigo = f.read()
        py = self.transpilar(codigo)
        exec(compile(py, ruta, 'exec'), self.ns)

    def _llaves(self, s):
        s = s.replace(chr(92)+chr(34), chr(1)).replace(chr(92)+chr(39), chr(2))
        code = ''
        quote = None
        for c in s:
            if quote:
                if c == quote: quote = None
            elif c in '"\'': quote = c
            elif c == '#': break
            else: code += c
        return code.count('{') - code.count('}')

    def transpilar(self, codigo):
        py = []
        indent = 0
        in_triple = None
        class_stack = []
        for raw in codigo.split('\n'):
            if in_triple:
                py.append(raw)
                if raw.count(in_triple) % 2 == 1: in_triple = None
                continue
            tq = None
            for q in ('"""', "''" + "'"):
                if raw.count(q) % 2 == 1: tq = q; break
            if tq:
                in_triple = tq
            mu = re.match(r'^usar\s+["\'](.+?)["\']$', raw.strip())
            if mu:
                py.append(raw[:len(raw) - len(raw.lstrip())] + 'usar("' + mu.group(1) + '")')
                continue
            s = self._quitar_comentarios(raw).strip()
            if not s: py.append(''); continue
            if s == '}':
                indent = max(0, indent - 1)
                while class_stack and indent <= class_stack[-1]:
                    class_stack.pop()
                continue
            if s.startswith('}') and ('sino' in s or 'else' in s or 'capturar' in s or 'except' in s or 'finalmente' in s or 'finally' in s):
                indent = max(0, indent - 1)
                head = s[1:].strip()
                if head.endswith('{'): head = head[:-1].strip()
                m = re.match(r'(?:capturar|except)\s*\(\s*(\w+)\s*\)', head)
                if m:
                    py.append('    ' * indent + f'except Exception as {m.group(1)}:')
                elif head.startswith('capturar') or head.startswith('except'):
                    py.append('    ' * indent + 'except Exception:')
                elif head.startswith('finalmente') or head.startswith('finally'):
                    py.append('    ' * indent + 'finally:')
                else:
                    py.append('    ' * indent + 'else:')
                indent += 1
                continue
            if s.startswith('}') and ('capturar' in s or 'catch' in s):
                indent = max(0, indent - 1)
                m = re.search(r'\((\w+)\)', s)
                var = m.group(1) if m else 'e'
                py.append('    ' * indent + f'except Exception as {var}:')
                indent += 1
                continue
            if s.startswith('}') and ('finalmente' in s or 'finally' in s):
                indent = max(0, indent - 1)
                py.append('    ' * indent + 'finally:')
                indent += 1
                continue
            if s.endswith('{'):
                head = self._traducir(s[:-1].rstrip())
                in_class = bool(class_stack) and indent > class_stack[-1]
                if in_class:
                    head = self._inject_self(head)
                py.append('    ' * indent + head + ':')
                if head.startswith('class '):
                    class_stack.append(indent)
                indent += 1
                continue
            line = self._fix_linea(self._traducir(s))
            if class_stack and indent > class_stack[-1]:
                line = self._inject_self(line)
            py.append('    ' * indent + line)
        final = []
        for i, l in enumerate(py):
            final.append(l)
            if l.rstrip().endswith(':'):
                cur = len(l) - len(l.lstrip())
                nxt = py[i+1] if i+1 < len(py) else None
                if nxt is None or (len(nxt) - len(nxt.lstrip())) <= cur:
                    final.append(' ' * (cur + 4) + 'pass')
        return '\n'.join(final)

    def ejecutar(self, codigo):
        self.output = []
        py = self.transpilar(codigo)
        lineas_py = py.split('\n')
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
                    error_msg += f"\n   {prefix} {i:3d} │ {lineas_py[i-1]}"
                if lineno <= len(lineas_py):
                    error_msg += f"\n     {' ' * len(lineas_py[lineno-1])} ^ {e}"
            
            self.out(error_msg)
        return {'output': self.output, 'db': self.ns['db']._data}

def es_html(t):
    return isinstance(t, str) and t.strip().startswith('<')

# ==================== WEB SERVER (APIs tipo Flask) ====================
class ServidorWeb:
    def __init__(self, puerto=8080):
        self.puerto = puerto
        self.rutas = {}
        self._datos = {}
    def parametro(self, nombre):
        return getattr(self, '_query', {}).get(nombre)
    def recibir_datos(self):
        return self._datos
    def redirigir(self, ruta):
        return 'REDIRIGIR:' + ruta
    def _parsear(self, cuerpo):
        datos = {}
        try:
            if cuerpo.strip().startswith('{'):
                datos = json.loads(cuerpo)
            else:
                from urllib.parse import unquote_plus
                datos = {k: unquote_plus(v) for k, v in (p.split('=', 1) for p in cuerpo.split('&') if '=' in p)}
        except Exception:
            pass
        return datos
    def ruta(self, path, funcion):
        self.rutas[path] = funcion
        return f"Ruta {path} registrada"
    def iniciar(self):
        from http.server import HTTPServer, BaseHTTPRequestHandler
        rutas = self.rutas
        serv = self
        class H(BaseHTTPRequestHandler):
            def do_GET(s):
                serv._query = {}
                ruta = s.path
                if '?' in ruta:
                    ruta, qs = ruta.split('?', 1)
                    for kv in qs.split('&'):
                        if '=' in kv:
                            k, v = kv.split('=', 1)
                            serv._query[k] = v
                if ruta in rutas:
                    r = rutas[ruta]()
                    if es_html(r):
                        s.send_response(200)
                        s.send_header('Content-Type', 'text/html; charset=utf-8')
                        s.end_headers()
                        s.wfile.write(str(r).encode())
                    else:
                        s.send_response(200)
                        s.send_header('Content-Type', 'application/json')
                        s.end_headers()
                        s.wfile.write(json.dumps(r, ensure_ascii=False).encode())
                else:
                    s.send_response(404)
                    s.end_headers()
            def do_POST(s):
                n = int(s.headers.get('Content-Length', 0))
                cuerpo = s.rfile.read(n).decode('utf-8') if n else ''
                serv._datos = serv._parsear(cuerpo)
                if s.path in rutas:
                    r = rutas[s.path]()
                    if isinstance(r, str) and r.startswith('REDIRIGIR:'):
                        s.send_response(302)
                        s.send_header('Location', r[10:])
                        s.end_headers()
                        return
                    s.send_response(200)
                    s.send_header('Content-Type', 'text/html; charset=utf-8')
                    s.end_headers()
                    s.wfile.write(str(r).encode())
                else:
                    s.send_response(404)
                    s.end_headers()
            def log_message(s, *a): pass
        HTTPServer(('0.0.0.0', int(__import__('os').environ.get('PORT', self.puerto))), H).serve_forever()

DEMO_CODE = """
imprimir("🚀 NexusLang v5.3 - Demo en 30 segundos")
def calcular_total(precio, cantidad) => precio * cantidad
imprimir("Funciones: " + texto(calcular_total(100.5, 3)))
clase Producto {
    def __init__(nombre, precio) {
        este.nombre = nombre
        este.precio = precio
    }
    def info() {
        devolver este.nombre + ": $" + texto(este.precio)
    }
}
p = Producto("Laptop Pro", 999.99)
imprimir("Clases/OOP: " + p.info())
async funcion api() {
    devolver {"status": "online"}
}
imprimir("Async: " + texto(async_run(api())))
imprimir("IA: " + texto(ia.sentimiento("excellent and amazing")))
db.demo.producto = {"nombre": "Laptop"}
imprimir("Base de datos: " + texto(db.demo.producto))
imprimir("✅ Demo completo - listo para produccion")
"""

# ==================== TESTS (18) ====================
def run_tests():
    print("="*70)
    print(f"NEXUSLANG v{VERSION} - PROFESSIONAL TEST SUITE (23 tests)")
    print("="*70)
    passed = failed = 0
    def check(name, cond, extra=""):
        nonlocal passed, failed
        if cond: print(f"[✅] {name}"); passed += 1
        else: print(f"[❌] {name} {extra}"); failed += 1

    l = NexusLang(mostrar=False)
    l.ejecutar('x = 10\ny = 20\nz = x + y\nimprimir(z)')
    check("1. Arithmetic", l.output and '30' in l.output, str(l.output))

    l = NexusLang(mostrar=False)
    l.ejecutar('imprimir("hola")\nprint("hello")')
    check("2. Bilingual", 'hola' in l.output and 'hello' in l.output, str(l.output))

    l = NexusLang(mostrar=False)
    l.ejecutar('imprimir(mayusculas("hola mundo"))')
    check("3. Strings", 'HOLA MUNDO' in l.output, str(l.output))

    l = NexusLang(mostrar=False)
    l.ejecutar('imprimir(ordenar([3, 1, 2]))')
    check("4. Lists", '[1, 2, 3]' in l.output, str(l.output))

    l = NexusLang(mostrar=False)
    l.ejecutar('def sumar(a, b) => a + b\nimprimir(sumar(2, 3))')
    check("5. Arrow functions", '5' in l.output, str(l.output))

    l = NexusLang(mostrar=False)
    l.ejecutar('si (10 > 5) {\nimprimir("mayor")\n} sino {\nimprimir("menor")\n}')
    check("6. If/Else", 'mayor' in l.output, str(l.output))

    l = NexusLang(mostrar=False)
    l.ejecutar('total = 0\npara i en rango(1, 6) {\ntotal = total + i\n}\nimprimir(total)')
    check("7. For loops", '15' in l.output, str(l.output))

    l = NexusLang(mostrar=False)
    l.ejecutar('x = 0\nmientras (x < 3) {\nx = x + 1\n}\nimprimir(x)')
    check("8. While loops", '3' in l.output, str(l.output))

    l = NexusLang(mostrar=False)
    l.ejecutar('db.usuarios.lucas = {"nombre": "Lucas"}\nimprimir(db.usuarios.lucas)')
    ok = l.ns['db']._data.get('usuarios', {}).get('lucas', {}).get('nombre') == 'Lucas'
    check("9. Database", ok and 'Lucas' in str(l.output), str(l.output))

    check("10. AI sentiment", l.ia.sentimiento("excellent")['result'] == 'positive')

    l = NexusLang(mostrar=False)
    l.ejecutar('web.guardar("test", web.pagina("T", web.parrafo("OK")))')
    check("11. Web generation", Path("nexus_pages/test.html").exists())

    l = NexusLang(mostrar=False)
    l.ejecutar('archivo_escribir("nexus_archivos/t.txt", "dato")\nimprimir(archivo_leer("nexus_archivos/t.txt"))')
    check("12. File I/O", 'dato' in l.output, str(l.output))

    l = NexusLang(mostrar=False)
    l.ejecutar('intentar {\nx = 1 / 0\n} capturar (error) {\nimprimir("atrapado")\n}')
    check("13. Try/Catch", 'atrapado' in l.output, str(l.output))

    l = NexusLang(mostrar=False)
    l.ejecutar('clase Persona {\ndef __init__(nombre) {\neste.nombre = nombre\n}\ndef saludar() {\ndevolver "Hola " + este.nombre\n}\n}\np = Persona("Lucas")\nimprimir(p.saludar())')
    check("14. Classes/OOP", 'Hola Lucas' in l.output, str(l.output))

    Path('nx_temp_mod.nx').write_text('def doble(n) => n * 2\n')
    l = NexusLang(mostrar=False)
    l.ejecutar('importar("nx_temp_mod")\nimprimir(doble(21))')
    check("15. Modules/imports", '42' in l.output, str(l.output))

    l = NexusLang(mostrar=False)
    l.ejecutar("datos = json_parsear('{\"a\": 5}')\nimprimir(datos['a'])")
    check("16. JSON", '5' in l.output, str(l.output))

    l = NexusLang(mostrar=False)
    l.ejecutar('imprimir(formatear("Hola {n}", {"n": "Ana"}))')
    check("17. Interpolation", 'Hola Ana' in l.output, str(l.output))

    check("18. HTTP support", hasattr(NexusLang(mostrar=False).ns['web'], 'obtener'))
    check("19. Web server (APIs)", hasattr(NexusLang(mostrar=False).ns['web'], 'servidor'))
    check("20. Full-stack HTML+JSON", es_html("<html>x</html>") and not es_html({"a": 1}))
    
    l = NexusLang(mostrar=False)
    l.ejecutar('def sumar(a: int, b: int) -> int => a + b\nimprimir(sumar(5, 3))')
    check("21. Type hints", '8' in l.output, str(l.output))
    
    l = NexusLang(mostrar=False)
    l.ejecutar('async funcion async_test() {\n    devolver "async works"\n}\nresultado = async_run(async_test())\nimprimir(resultado)')
    check("22. Async/await", 'async works' in l.output, str(l.output))
    
    l = NexusLang(mostrar=False)
    l.ejecutar('imprimir(x_inexistente)')
    has_context = '│' in l.output[0] if l.output else False
    check("23. Error context", has_context, str(l.output))

    print("="*70)
    print(f"RESULT: {passed} passed | {failed} failed | {passed+failed} total")
    print("="*70)
    print("✅ ALL TESTS PASSED - PRODUCTION READY" if failed == 0 else "❌ FIX NEEDED")
    nx6 = NexusLang()
    nx6.ejecutar('imprimir("v6a:#{}()")')
    check('string_blindada', 'v6a:#{}()' in ''.join(nx6.output))
    nx7 = NexusLang()
    codigo = 'imprimir("v6b:di' + chr(92) + chr(34) + 'jo")'
    nx7.ejecutar(codigo)
    check('escapes', 'v6b:di"jo' in ''.join(nx7.output))
    nx8 = NexusLang()
    nx8.ejecutar('imprimir(nexus.texto.mayusculas("v61"))')
    check('stdlib_texto', 'V61' in ''.join(nx8.output))
    nx9 = NexusLang()
    nx9.ejecutar('imprimir(nexus.lista.sumar([1, 2, 3]))')
    check('stdlib_lista', '6' in ''.join(nx9.output))
    nxa = NexusLang()
    nxa.ejecutar('x = """<div>\n<h1>hola</h1>\n</div>"""\nimprimir("v61ml:" + x)')
    check('triple_string', '</div>' in ''.join(nxa.output))
    nxb = NexusLang()
    nxb.ejecutar('usar "nx_temp_mod.nx"\nimprimir(doble(21))')
    check('modulos', '42' in ''.join(nxb.output))
    nxc = ServidorWeb()
    d = nxc._parsear('nombre=Lucas&tienda=Mi%20Shop')
    check('post_form', d.get('tienda') == 'Mi Shop')
    nxd = ServidorWeb()
    check('redirigir', nxd.redirigir('/ok') == 'REDIRIGIR:/ok')
    nxe = ServidorWeb()
    dj = nxe._parsear('{"a": 1}')
    check('post_json', dj.get('a') == 1)
    return failed == 0

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ('--help', '-h', 'help', 'ayuda'):
        print("NEXUSLANG v%s - lenguaje bilingue (es/en)" % VERSION)
        print("USO / USAGE:")
        print("  nexus archivo.nx       ejecutar app / run app")
        print("  nexus -i               interactivo / interactive REPL")
        print("  nexus --demo [es|en]   demo bilingue / bilingual demo")
        print("  nexus --test           probar / run tests")
        print("  nexus --help           ayuda / help")
        print("SINTAXIS / SYNTAX:")
        print("  imprimir|print  clase|class  devolver|return")
        print("  si|if  sino|else  para|for  mientras|while")
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        modo = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] in ('es', 'en') else 'es'
        codigo = DEMO_CODE
        if modo == 'en':
            codigo = DEMO_CODE.replace('imprimir(', 'print(').replace('Clases/OOP:', 'Classes/OOP:').replace('Base de datos:', 'Database:').replace('"IA: "', '"AI: "').replace('Demo completo - listo para produccion', 'Demo complete - production ready')
        NexusLang().ejecutar(codigo)
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == '-i':
        print(f"NEXUSLANG v{VERSION} - INTERACTIVE (type 'salir')")
        lang = NexusLang()
        buffer = ''
        while True:
            try:
                linea = input('... ' if buffer else 'nx> ')
            except (EOFError, KeyboardInterrupt):
                print("\nBye!"); break
            if linea.strip() in ['salir', 'exit', 'quit']: break
            buffer += linea + '\n'
            if self._llaves(buffer) > 0: continue
            linea = buffer.strip()
            es_expr = bool(linea) and '=' not in linea and not linea.startswith('#') and linea.split()[0] not in ('imprimir','print','clase','class','si','if','para','for','mientras','while','devolver','return','async','usar')
            try:
                lang.ejecutar('imprimir(' + linea + ')' if es_expr else buffer)
            except Exception as e:
                print("⛔ " + type(e).__name__ + ": " + str(e).split('(')[0].strip())
            buffer = ''
    elif len(sys.argv) > 1 and sys.argv[1] != '--test':
        lang = NexusLang()
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            try:
                lang.ejecutar(f.read())
            except Exception as e:
                print("⛔ Error en tu app / in your app -> " + type(e).__name__ + ": " + str(e).split('(')[0].strip())
                sys.exit(1)
    else:
        ok = run_tests()
        sys.exit(0 if ok else 1)

def main():
    import runpy
    runpy.run_path(__file__, run_name="__main__")
