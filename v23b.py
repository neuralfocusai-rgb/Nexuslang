src = open('nexusshop/v20.nx').read()
old = open('old_tienda.nx').read()
new = open('new_tienda.nx').read()
def rep(o, n, tag):
    global src
    c = src.count(o)
    print(tag, '->', c)
    if c == 1: src = src.replace(o, n, 1)
rep(old, new, 'tienda_completa')
rep("placeholder='Emoji (ej: 🍕)' style='padding:12px;background:#1a1a2a;border:1px solid #2a2a3a;border-radius:8px;color:#fff'>", "placeholder='Emoji (ej: 🍕)' style='padding:12px;background:#1a1a2a;border:1px solid #2a2a3a;border-radius:8px;color:#fff'>\n    html = html + \"<input name='foto' placeholder='URL de foto (opcional)' style='padding:12px;background:#1a1a2a;border:1px solid #2a2a3a;border-radius:8px;color:#fff'>\"", 'campo_foto')
rep("""    shop.agregar_producto(slug, nombre, precio, emoji, "panel", 0, 0)
    shop.guardar()""", """    shop.agregar_producto(slug, nombre, precio, emoji, "panel", 0, 0)
    foto = d.get("foto", "")
    si foto != "" {
        shop.tiendas[slug]["productos"][-1]["foto"] = foto
    }
    shop.guardar()""", 'guarda_foto')
rep('s.ruta("/panel-agregar", panel_agregar)', 's.ruta("/panel-agregar", panel_agregar)\ns.ruta("/buscar", lambda: T(pagina_buscar()))\ns.ruta("/resenar", resenar)', 'rutas_v23')
rep("EN</a></div></body>", "EN</a><form method='GET' action='/buscar' style='display:inline;margin-left:10px'><input name='q' placeholder='🔍' style='padding:6px;border-radius:6px;border:1px solid #2a2a3a;background:#1a1a2a;color:#fff;width:70px'></form></div></body>", 'busca_en_barra')
open('nexusshop/v20.nx','w').write(src)
print('PATCH v2.3 OK')
