import re
src = open('nexuslang.py').read()
def rep(old, new, tag):
    global src
    n = src.count(old)
    print(tag, '->', n)
    if n == 1: src = src.replace(old, new, 1)

rep("    def recibir_datos(self):", "    def parametro(self, nombre):\n        return getattr(self, '_query', {}).get(nombre)\n    def recibir_datos(self):", 'parametro')

rep("""            def do_GET(s):
                if s.path in rutas:
                    r = rutas[s.path]()""", """            def do_GET(s):
                serv._query = {}
                ruta = s.path
                if '?' in ruta:
                    ruta, qs = ruta.split('?', 1)
                    for kv in qs.split('&'):
                        if '=' in kv:
                            k, v = kv.split('=', 1)
                            serv._query[k] = v
                if ruta in rutas:
                    r = rutas[ruta]()""", 'query_get')

rep('VERSION = "6.2.0"', 'VERSION = "6.3.0"', 'version')
open('nexuslang.py','w').write(src)
print('MOTOR v6.3 OK')

src = open('nexusshop/v20.nx').read()

T_FUNC = '''def T(html) {
    si s.parametro("lang") != "en" {
        devolver html
    }
    html = html.replace("Pedir por WhatsApp", "Order via WhatsApp").replace("Creá tu tienda", "Create your store").replace("Crear tienda gratis", "Create free store").replace("Nombre de la tienda", "Store name").replace("Tu WhatsApp (con código de país)", "Your WhatsApp (with country code)").replace(" productos</p>", " products</p>").replace("Tecnologia", "Technology").replace("Alimentos", "Food").replace("Educación", "Education").replace("Moda", "Fashion").replace("Salud", "Health").replace("Envíos", "Shipping").replace("Ayuda", "Help").replace("Confianza", "Trust").replace("Privacidad", "Privacy").replace("Nosotros", "About us").replace("Beneficios", "Benefits")
    html = html.replace("</body>", "<div style='position:fixed;bottom:0;left:0;right:0;background:#0a0a0f;border-top:1px solid #2a2a3a;padding:10px;text-align:center;z-index:99'><a href='?lang=es' style='color:#fff;text-decoration:none;margin:0 10px'>🇪🇸 ES</a><a href='?lang=en' style='color:#00d4ff;text-decoration:none;margin:0 10px'>🇬 EN</a></div></body>")
    devolver html
}

'''
print('T_func ->', 'def pagina_crear' in src)
src = src.replace('def pagina_crear', T_FUNC + 'def pagina_crear', 1)

def wrap(m):
    name = m.group(1)
    if name == 'api' or name.startswith('k_'):
        return m.group(0)
    return 'def %s() => T(%s)' % (name, m.group(2))
src2 = re.sub(r'^(def \w+\(\) => )(shop\.\S+)$', lambda m: m.group(0) if (m.group(0).split('def ')[1].split('(')[0] == 'api' or m.group(0).split('def ')[1].startswith('k_')) else m.group(1).replace('=> ', '=> T(') + m.group(2) + ')', src, flags=re.M)
src = src2

src = src.replace('s.ruta("/crear", pagina_crear)', 's.ruta("/crear", lambda: T(pagina_crear()))')
src = src.replace('s.ruta("/comprar/" + slug, lambda sl=slug: pagina_tienda_nueva(sl))', 's.ruta("/comprar/" + slug, lambda sl=slug: T(pagina_tienda_nueva(sl)))')
open('nexusshop/v20.nx','w').write(src)
print('MARKETPLACE v2.1 OK')
