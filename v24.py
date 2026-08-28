src = open('nexusshop/v20.nx').read()
def rep(old, new, tag):
    global src
    n = src.count(old)
    print(tag, '->', n)
    if n == 1: src = src.replace(old, new, 1)

rep('def pagina_crear', '''def panel_pago() {
    d = s.recibir_datos()
    slug = d.get("slug", "")
    pin = d.get("pin", "")
    si pin_ok(slug, pin) == 0 {
        devolver s.redirigir("/panel")
    }
    shop.tiendas[slug]["pago"] = d.get("pago", "")
    shop.guardar()
    devolver s.redirigir("/panel?slug=" + slug + "&pin=" + pin)
}

def pagina_crear''', 'panel_pago')

rep("    html = html + \"<h2 style='color:#00d4ff'>📦 Tu catálogo (\" + texto(len(t[\"productos\"])) + \")</h2>\"", "    html = html + \"<h2 style='color:#00d4ff'>💳 Tu link de pago</h2>\"\n    html = html + \"<form method='POST' action='/panel-pago' style='display:flex;gap:8px;max-width:400px'><input type='hidden' name='slug' value='\" + slug + \"'><input type='hidden' name='pin' value='\" + pin + \"'><input name='pago' placeholder='https://mpago.la/tu-link' style='flex:1;padding:10px;background:#1a1a2a;border:1px solid #2a2a3a;border-radius:8px;color:#fff'><button style='padding:10px;background:#0f0;border:none;border-radius:8px;color:#000;font-weight:700'>Guardar</button></form>\"\n    html = html + \"<h2 style='color:#00d4ff'>📦 Tu catálogo (\" + texto(len(t[\"productos\"])) + \")</h2>\"", 'form_pago_panel')

rep("    html = html + \"<a href='https://wa.me/\" + t[\"whatsapp\"] + \"' style='color:#0f0'>💬 Pedir por WhatsApp</a>\"", "    html = html + \"<a href='https://wa.me/\" + t[\"whatsapp\"] + \"' style='color:#0f0'>💬 Pedir por WhatsApp</a>\"\n    si t.get(\"pago\", \"\") != \"\" {\n        html = html + \" <a href='\" + t[\"pago\"] + \"' style='color:#00d4ff;margin-left:10px'>💳 Pagar online</a>\"\n    }", 'boton_pago')

rep('s.ruta("/resenar", resenar)', 's.ruta("/resenar", resenar)\ns.ruta("/panel-pago", panel_pago)', 'ruta_pago')

open('nexusshop/v20.nx','w').write(src)
print('PATCH v2.4 OK')
