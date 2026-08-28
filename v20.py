src = open('nexusshop/v19.nx').read()

FORM = '''web.ruta("/crear", lambda: """<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Crear tienda - NexusShop</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0f;color:#e0e0e0;font-family:system-ui,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh}
form{background:#12121a;border:1px solid #2a2a3a;border-radius:16px;padding:2rem;width:90%;max-width:400px}
h1{color:#00d4ff;margin-bottom:1.5rem;text-align:center;font-size:1.5rem}
label{display:block;margin:1rem 0 .3rem;color:#888;font-size:.9rem}
input{width:100%;padding:.8rem;background:#1a1a2a;border:1px solid #2a2a3a;border-radius:8px;color:#fff;font-size:1rem}
input:focus{outline:none;border-color:#00d4ff}
button{width:100%;margin-top:1.5rem;padding:1rem;background:linear-gradient(135deg,#00d4ff,#0088cc);border:none;border-radius:8px;color:#000;font-weight:700;font-size:1rem;cursor:pointer}
button:hover{opacity:.9}
</style></head><body>
<form method="POST" action="/crear-ok">
<h1>🛒 Creá tu tienda</h1>
<label>Nombre de la tienda</label>
<input name="nombre" required placeholder="Mi Shop">
<label>Tu WhatsApp (con código de país)</label>
<input name="whatsapp" required placeholder="+5491123456789">
<button>Crear tienda gratis</button>
</form></body></html>""")

web.ruta("/crear-ok", lambda: (lambda d: app.crear_tienda(d.get("nombre",""), d.get("whatsapp","")) or web.redirigir("/tienda/" + d.get("nombre","").replace(" ","-").lower()))(web.recibir_datos()))
'''

marker = 'web.iniciar(puerto=8104)'
if marker not in src:
    print('ERROR: no encuentro web.iniciar')
else:
    src = src.replace(marker, FORM + '\n' + marker)
    open('nexusshop/v20.nx', 'w').write(src)
    print('v20.nx CREADO OK')
