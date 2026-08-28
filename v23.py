src = open('nexusshop/v20.nx').read()
def rep(old, new, tag):
    global src
    n = src.count(old)
    print(tag, '->', n)
    if n == 1: src = src.replace(old, new, 1)

rep("placeholder='Emoji (ej: 🍕)' style='padding:12px;background:#1a1a2a;border:1px solid #2a2a3a;border-radius:8px;color:#fff'>", "placeholder='Emoji (ej: 🍕)' style='padding:12px;background:#1a1a2a;border:1px solid #2a2a3a;border-radius:8px;color:#fff'>\n    html = html + \"<input name='foto' placeholder='URL de foto (opcional)' style='padding:12px;background:#1a1a2a;border:1px solid #2a2a3a;border-radius:8px;color:#fff'>\"", 'campo_foto')

rep("""    shop.agregar_producto(slug, nombre, precio, emoji, "panel", 0, 0)
    shop.guardar()""", """    shop.agregar_producto(slug, nombre, precio, emoji, "panel", 0, 0)
    foto = d.get("foto", "")
    si foto != "" {
        shop.tiendas[slug]["productos"][-1]["foto"] = foto
    }
    shop.guardar()""", 'guarda_foto')

rep("""def pagina_tienda_nueva(sl) {
    t = shop.tiendas[sl]
    devolver "<html><head><meta name='viewport' content='width=device-width,initial-scale=1'></head><body style='background:#0a0a0f;color:#e0e0e0;font-family:system-ui;padding:20px'><h1 style='color:#00d4ff'>" + t["emoji"] + " " + t["nombre"] + "</h1><p>⭐ " + t["estrellas"] + " · " + texto(len(t["productos"])) + " productos</p><a href='https://wa.me/" + t["whatsapp"] + "' style='color:#0f0'>💬 Pedir por WhatsApp</a></body></html>"
}""", """def promedio_estrellas(sl) {
    r = shop.tiendas[sl].get("resenas", [])
    si len(r) == 0 {
        devolver "5.0"
    }
    i = 0
    suma = 0
    mientras i < len(r) {
        suma = suma + r[i]["estrellas"]
        i = i + 1
    }
    devolver texto(suma / len(r)) + " (" + texto(len(r)) + " reseñas)"
}

def lista_resenas(sl) {
    r = shop.tiendas[sl].get("resenas", [])
    i = 0
    html = ""
    mientras i < len(r) {
        html = html + "<p style='border-bottom:1px solid #2a2a3a;padding:6px'>⭐" + texto(r[i]["estrellas"]) + " — " + r[i]["comentario"] + "</p>"
        i = i + 1
    }
    devolver html
}

def pagina_buscar() {
    q = s.parametro("q")
    si q == None {
        q = ""
    }
    q = q.lower()
    html = "<html><head><meta name='viewport' content='width=device-width,initial-scale=1'></head><body style='background:#0a0a0f;color:#e0e0e0;font-family:system-ui;padding:20px'><h1 style='color:#00d4ff'>🔍 " + q + "</h1>"
    j = 0
    mientras j < len(shop.slugs) {
        sl = shop.slugs[j]
        t = shop.tiendas[sl]
        i = 0
        mientras i < len(t["productos"]) {
            p = t["productos"][i]
            si q != "" {
                si p["nombre"].lower().find(q) != -1 {
                    html = html + "<p><a href='/comprar/" + sl + "' style='color:#00d4ff'>" + t["nombre"] + "</a> · " + p["emoji"] + " " + p["nombre"] + " — $" + texto(p["precio"]) + "</p>"
                }
            }
            i = i + 1
        }
        j = j + 1
    }
    html = html + "</body></html>"
    devolver html
}

def resenar() {
    d = s.recibir_datos()
    slug = d.get("slug", "")
    si shop.tiendas.get(slug) == None {
        devolver s.redirigir("/")
    }
    estrellas = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5}.get(d.get("estrellas", "5"), 5)
    si shop.tiendas[slug].get("resenas") == None {
        shop.tiendas[slug]["resenas"] = []
    }
    shop.tiendas[slug]["resenas"] = shop.tiendas[slug]["resenas"] + [{"estrellas": estrellas, "comentario": d.get("comentario", "")}]
    shop.guardar()
    devolver s.redirigir("/comprar/" + slug)
}

def pagina_tienda_nueva(sl) {
    t = shop.tiendas[sl]
    html = "<html><head><meta name='viewport' content='width=device-width,initial-scale=1'></head><body style='background:#0a0a0f;color:#e0e0e0;font-family:system-ui;padding:20px'>"
    html = html + "<h1 style='color:#00d4ff'>" + t["emoji"] + " " + t["nombre"] + "</h1>"
    html = html + "<p>⭐ " + promedio_estrellas(sl) + " · " + texto(len(t["productos"])) + " productos</p>"
    html = html + "<a href='https://wa.me/" + t["whatsapp"] + "' style='color:#0f0'>💬 Pedir por WhatsApp</a>"
    i = 0
    mientras i < len(t["productos"]) {
        p = t["productos"][i]
        html = html + "<div style='border:1px solid #2a2a3a;border-radius:12px;padding:12px;margin:12px 0;display:flex;gap:12px;align-items:center'>"
        si p.get("foto", "") != "" {
            html = html + "<img src='" + p["foto"] + "' style='width:70px;height:70px;object-fit:cover;border-radius:8px'>"
        }
        si p.get("foto", "") == "" {
            html = html + "<span style='font-size:40px'>" + p["emoji"] + "</span>"
        }
        html = html + "<div><b>" + p["nombre"] + "</b><br>$ " + texto(p["precio"]) + "<br><a href='https://wa.me/" + t["whatsapp"] + "?text=" + p["nombre"].replace(" ", "%20") + "' style='color:#0f0'>Pedir este producto</a></div></div>"
        i = i + 1
    }
    html = html + "<h2 style='color:#00d4ff'>✍️ Dejá tu reseña</h2>"
    html = html + "<form method='POST' action='/resenar' style='display:flex;gap:8px;max-width:400px'><input type='hidden' name='slug' value='" + sl + "'><select name='estrellas' style='padding:10px;background:#1a1a2a;border:1px solid #2a2a3a;border-radius:8px;color:#fff'><option>5</option><option>4</option><option>3</option><option>2</option><option>1</option></select><input name='comentario' placeholder='Tu experiencia' style='flex:1;padding:10px;background:#1a1a2a;border:1px solid #2a2a3a;border-radius:8px;color:#fff'><button style='padding:10px;background:#00d4ff;border:none;border-radius:8px;color:#000;font-weight:700'>Enviar</button></form>"
    html = html + lista_resenas(sl) + "</body></html>"
    devolver html
}""', 'tienda_completa')

rep('s.ruta("/panel-agregar", panel_agregar)', '''s.ruta("/panel-agregar", panel_agregar)
s.ruta("/buscar", lambda: T(pagina_buscar()))
s.ruta("/resenar", resenar)''', 'rutas_v23')

rep("EN</a></div></body>", "EN</a><form method='GET' action='/buscar' style='display:inline;margin-left:10px'><input name='q' placeholder='🔍' style='padding:6px;border-radius:6px;border:1px solid #2a2a3a;background:#1a1a2a;color:#fff;width:70px'></form></div></body>", 'busca_en_barra')

open('nexusshop/v20.nx','w').write(src)
print('PATCH v2.3 OK')
