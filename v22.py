src = open('nexusshop/v20.nx').read()
def rep(old, new, tag):
    global src
    n = src.count(old)
    print(tag, '->', n)
    if n == 1: src = src.replace(old, new, 1)

rep('def pagina_crear', '''def pin_ok(slug, pin) {
    t = shop.tiendas.get(slug)
    si t == None {
        devolver 0
    }
    si t.get("pin", "") != pin {
        devolver 0
    }
    si pin == "" {
        devolver 0
    }
    devolver 1
}

def pagina_panel() {
    slug = s.parametro("slug")
    pin = s.parametro("pin")
    si slug == None {
        slug = ""
    }
    si pin == None {
        pin = ""
    }
    si pin_ok(slug, pin) == 0 {
        devolver "<html><head><meta name='viewport' content='width=device-width,initial-scale=1'></head><body style='background:#0a0a0f;color:#e0e0e0;font-family:system-ui;display:flex;justify-content:center;align-items:center;min-height:100vh'><form method='GET' action='/panel' style='background:#12121a;border:1px solid #2a2a3a;border-radius:16px;padding:2rem;width:90%;max-width:400px'><h1 style='color:#00d4ff;text-align:center'>🛠️ Panel del vendedor</h1><input name='slug' placeholder='tu-tienda' required style='width:100%;padding:12px;margin:8px 0;background:#1a1a2a;border:1px solid #2a2a3a;border-radius:8px;color:#fff'><input name='pin' placeholder='PIN' required style='width:100%;padding:12px;margin:8px 0;background:#1a1a2a;border:1px solid #2a2a3a;border-radius:8px;color:#fff'><button style='width:100%;padding:14px;background:linear-gradient(135deg,#00d4ff,#0088cc);border:none;border-radius:8px;color:#000;font-weight:700'>Entrar</button></form></body></html>"
    }
    t = shop.tiendas[slug]
    html = "<html><head><meta name='viewport' content='width=device-width,initial-scale=1'></head><body style='background:#0a0a0f;color:#e0e0e0;font-family:system-ui;padding:20px'>"
    html = html + "<h1 style='color:#00d4ff'>🛠️ Panel de " + t["nombre"] + "</h1>"
    html = html + "<p style='color:#888'>Tu PIN: <b style='color:#0f0'>" + pin + "</b> — guardalo para volver a entrar</p>"
    html = html + "<h2 style='color:#00d4ff'>➕ Agregar producto</h2>"
    html = html + "<form method='POST' action='/panel-agregar' style='display:flex;flex-direction:column;gap:10px;max-width:400px'>"
    html = html + "<input type='hidden' name='slug' value='" + slug + "'>"
    html = html + "<input type='hidden' name='pin' value='" + pin + "'>"
    html = html + "<input name='nombre' placeholder='Nombre del producto' required style='padding:12px;background:#1a1a2a;border:1px solid #2a2a3a;border-radius:8px;color:#fff'>"
    html = html + "<input name='precio' placeholder='Precio' required style='padding:12px;background:#1a1a2a;border:1px solid #2a2a3a;border-radius:8px;color:#fff'>"
    html = html + "<input name='emoji' placeholder='Emoji (ej: 🍕)' style='padding:12px;background:#1a1a2a;border:1px solid #2a2a3a;border-radius:8px;color:#fff'>"
    html = html + "<button style='padding:14px;background:linear-gradient(135deg,#00d4ff,#0088cc);border:none;border-radius:8px;color:#000;font-weight:700'>Publicar producto</button></form>"
    html = html + "<h2 style='color:#00d4ff'>📦 Tu catálogo (" + texto(len(t["productos"])) + ")</h2>"
    i = 0
    lista = ""
    mientras i < len(t["productos"]) {
        p = t["productos"][i]
        lista = lista + "<p style='border-bottom:1px solid #2a2a3a;padding:8px'>" + p["emoji"] + " " + p["nombre"] + " — $" + texto(p["precio"]) + "</p>"
        i = i + 1
    }
    html = html + lista + "</body></html>"
    devolver html
}

def panel_agregar() {
    d = s.recibir_datos()
    slug = d.get("slug", "")
    pin = d.get("pin", "")
    si pin_ok(slug, pin) == 0 {
        devolver s.redirigir("/panel")
    }
    nombre = d.get("nombre", "")
    precio = d.get("precio", "0")
    emoji = d.get("emoji", "🛒")
    shop.agregar_producto(slug, nombre, precio, emoji, "panel", 0, 0)
    shop.guardar()
    devolver s.redirigir("/panel?slug=" + slug + "&pin=" + pin)
}

def pagina_crear''', 'funciones_panel')

rep("""    shop.crear_tienda(slug, nombre, wa, "🛒", "5.0", 0, "coordinado")
    shop.guardar()""", """    pin = texto((len(nombre) * 137 + len(wa) * 91) % 9000 + 1000)
    shop.crear_tienda(slug, nombre, wa, "🛒", "5.0", 0, "coordinado")
    shop.tiendas[slug]["pin"] = pin
    shop.guardar()""", 'pin_creacion')

rep('devolver s.redirigir("/comprar/" + slug)', 'devolver s.redirigir("/panel?slug=" + slug + "&pin=" + pin)', 'redirect_panel')

rep('s.ruta("/crear", lambda: T(pagina_crear()))', '''s.ruta("/crear", lambda: T(pagina_crear()))
s.ruta("/panel", lambda: T(pagina_panel()))
s.ruta("/panel-agregar", panel_agregar)''', 'rutas_panel')

open('nexusshop/v20.nx','w').write(src)
print('PATCH v2.2 OK')
