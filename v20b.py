import re
src = open('nexusshop/v19.nx').read()
ms = list(re.finditer(r'^\s*(\w+)\.iniciar\(', src, re.M))
if not ms:
    print('ERROR: sin iniciar')
else:
    sv = ms[-1].group(1)
    print('servidor detectado:', sv)
    FORM = '''def pagina_crear() {
    devolver """<!DOCTYPE html>
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
</style></head><body>
<form method="POST" action="/crear-ok">
<h1>🛒 Creá tu tienda</h1>
<label>Nombre de la tienda</label>
<input name="nombre" required placeholder="Mi Shop">
<label>Tu WhatsApp (con código de país)</label>
<input name="whatsapp" required placeholder="+5491123456789">
<button>Crear tienda gratis</button>
</form></body></html>"""
}

def pagina_tienda_nueva(sl) {
    t = shop.tiendas[sl]
    devolver "<html><head><meta name='viewport' content='width=device-width,initial-scale=1'></head><body style='background:#0a0a0f;color:#e0e0e0;font-family:system-ui;padding:20px'><h1 style='color:#00d4ff'>" + t["emoji"] + " " + t["nombre"] + "</h1><p>⭐ " + t["estrellas"] + " · " + texto(len(t["productos"])) + " productos</p><a href='https://wa.me/" + t["whatsapp"] + "' style='color:#0f0'>💬 Pedir por WhatsApp</a></body></html>"
}

def crear_ok() {
    d = @SV@.recibir_datos()
    nombre = d.get("nombre", "")
    wa = d.get("whatsapp", "")
    slug = nombre.replace(" ", "-").lower()
    shop.crear_tienda(slug, nombre, wa, "🛒", "5.0", 0, "coordinado")
    shop.guardar()
    @SV@.ruta("/comprar/" + slug, lambda sl=slug: pagina_tienda_nueva(sl))
    devolver @SV@.redirigir("/comprar/" + slug)
}

@SV@.ruta("/crear", pagina_crear)
@SV@.ruta("/crear-ok", crear_ok)
'''.replace('@SV@', sv)
    m = ms[-1]
    src = src[:m.start()] + FORM + src[m.start():]
    open('nexusshop/v20.nx', 'w').write(src)
    print('v20.nx CREADO OK')
