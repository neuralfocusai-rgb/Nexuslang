  }

  def resultados(q, theme) {
    res = este.buscar(q)
    rel = este.relacionadas(q)
    ai = ia.sentimiento(q)
    otro = "dark"
    si theme == "dark" { otro = "light" }
    html = este.head(theme, "<div class='wrap'><div class='topbar'><a href='/?t=" + theme + "' class='mini-logo'>🦅</a><form action='/buscar' style='flex:1'><input type='hidden' name='t' value='" + theme + "'><div class='searchbar'>🔍<input name='q' value='" + q + "'></div></form><a class='toggle' href='/buscar?q=" + q + "&t=" + otro + "'>🌙 " + otro + "</a></div>")
    html = html + "<div class='stats'>" + texto(len(res)) + " sovereign results · 3 sources · no logs · no trackers</div>"
    html = html + "<div class='cols'><div class='main'>"
    para r en res { html = html + este.tarjeta(r) }
    html = html + "<div class='related'><b>Related:</b><br>"
    para t en rel { html = html + "<a href='/buscar?q=" + t + "&t=" + theme + "'>" + t + "</a>" }
    html = html + "</div></div>"
    html = html + "<div class='panel'><div class='card'><span class='badge'>🦅 SOVEREIGN AI</span><h3 style='margin:12px 0 6px'>" + q + "</h3><p style='font-size:14px;line-height:1.5'>Nexus AI insight: " + texto(ai) + "</p><hr style='margin:12px 0'><p style='font-size:13px;color:#5f6368'>Falcon never logs your searches. Your data stays yours. Built with NexusLang — the bilingual language.</p><p style='font-size:13px;margin-top:8px'>🔎 Total sovereign searches: " + texto(db.falcon.stats.busquedas) + "</p></div></div></div>"
    html = html + "<div class='foot'>🦅 FalconSearch — See everything. Track nothing. · Powered by NexusLang</div></div></body></html>"
    devolver html
  }
}

motor = FalconSearch()
servidor = web.servidor(8080)

servidor.ruta("/", funcion(params) {
  theme = "light"
  si params["t"] == "dark" { theme = "dark" }
  devolver web.pagina(motor.home(theme))
})

servidor.ruta("/buscar", funcion(params) {
  theme = "light"
  si params["t"] == "dark" { theme = "dark" }
  db.falcon.stats.busquedas = db.falcon.stats.busquedas + 1
  devolver web.pagina(motor.resultados(params["q"], theme))
})

imprimir("✅ FalconSearch en http://localhost:8080")
EOF

python nexuslang.py falcon/falcon.nx
cd ~ && cat > falcon/falcon.nx << 'EOF'
# ==========================================
# FALCON SEARCH v0.6 - The Sovereign Search
# Google-grade UX, sovereign soul.
# Built 100% with NexusLang
# ==========================================
importar web
importar json
importar ia

clase FalconSearch {
  def __init__() {
    este.lema = "See everything. Track nothing."
    db.falcon.stats = {"busquedas": 0, "soberano": verdadero}
    imprimir("🦅 FalconSearch v0.6 - The Sovereign Search")
  }

  def colores(theme) {
    si theme == "dark" {
      devolver {"bg": "#0f1419", "text": "#e8eaed", "muted": "#9aa0a6", "card": "#171d26", "border": "#2a3240", "link": "#8ab4f8", "url": "#8ab4f8", "chip": "#171d26", "input": "#171d26"}
    }
    devolver {"bg": "#ffffff", "text": "#202124", "muted": "#5f6368", "card": "#ffffff", "border": "#dfe1e5", "link": "#0b57d0", "url": "#188038", "chip": "#f1f3f4", "input": "#ffffff"}
  }

  def head(c, titulo) {
    devolver "<!DOCTYPE html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>" + titulo + "</title></head><body style='margin:0;background:" + c["bg"] + ";color:" + c["text"] + ";font-family:Arial,system-ui,sans-serif'>"
  }

  def barra(q, c, theme) {
    devolver "<form action='/buscar' style='flex:1'><input type='hidden' name='t' value='" + theme + "'><div style='display:flex;align-items:center;gap:10px;border:1px solid " + c["border"] + ";border-radius:28px;padding:10px 18px;background:" + c["input"] + "'>🔍<input name='q' value='" + q + "' style='flex:1;border:none;outline:none;font-size:16px;background:transparent;color:" + c["text"] + "'></div></form>"
  }

  def buscar_wikipedia_es(q) {
    datos = json_parsear(web.obtener("https://es.wikipedia.org/w/api.php?action=query&list=search&srsearch=" + q + "&format=json"))
    r = []
    para item en datos["query"]["search"] {
      r.agregar({"titulo": item["title"], "desc": "Enciclopedia libre en español", "url": "https://es.wikipedia.org/wiki/" + item["title"], "fuente": "🇪🇸 Wikipedia"})
    }
    devolver r
  }

  def buscar_wikipedia_en(q) {
    datos = json_parsear(web.obtener("https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=" + q + "&format=json"))
    r = []
    para item en datos["query"]["search"] {
      r.agregar({"titulo": item["title"], "desc": "The free encyclopedia", "url": "https://en.wikipedia.org/wiki/" + item["title"], "fuente": "🇬 Wikipedia"})
    }
    devolver r
  }

  def buscar_duckduckgo(q) {
    datos = json_parsear(web.obtener("https://api.duckduckgo.com/?q=" + q + "&format=json&no_html=1"))
    r = []
    si datos["AbstractText"] != "" {
      r.agregar({"titulo": datos["Heading"], "desc": datos["AbstractText"], "url": datos["AbstractURL"], "fuente": "🦆 DuckDuckGo"})
    }
    devolver r
  }

  def buscar(q) {
    todos = []
    intentar { todos = todos + este.buscar_wikipedia_es(q) } capturar (e) { imprimir("⚠️ ES offline") }
    intentar { todos = todos + este.buscar_wikipedia_en(q) } capturar (e) { imprimir("⚠️ EN offline") }
    intentar { todos = todos + este.buscar_duckduckgo(q) } capturar (e) { imprimir("⚠️ DDG offline") }
    devolver todos
  }

  def relacionadas(q) {
    intentar {
      datos = json_parsear(web.obtener("https://es.wikipedia.org/w/api.php?action=opensearch&search=" + q + "&limit=6&format=json"))
      devolver datos[1]
    } capturar (e) { devolver [] }
  }

  def home(theme) {
    c = este.colores(theme)
    html = este.head(c, "Falcon Search")
    html = html + "<div style='min-height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:center;padding:20px'>"
    html = html + "<div style='font-size:72px'>🦅</div>"
    html = html + "<div style='font-size:46px;font-weight:bold;letter-spacing:-1px'><span style='color:#f59e0b'>F</span><span style='color:#0b57d0'>a</span><span style='color:#188038'>l</span><span style='color:#ea4335'>c</span><span style='color:#0b57d0'>o</span><span style='color:#f59e0b'>n</span></div>"
    html = html + "<div style='color:" + c["muted"] + ";margin:8px 0 26px;font-size:15px'>" + este.lema + "</div>"
    html = html + "<form action='/buscar'><input type='hidden' name='t' value='" + theme + "'><div style='display:flex;align-items:center;gap:10px;width:100%;max-width:580px;border:1px solid " + c["border"] + ";border-radius:28px;padding:12px 18px;background:" + c["input"] + "'>🔍<input name='q' autofocus placeholder='Search the sovereign web...' style='flex:1;border:none;outline:none;font-size:16px;background:transparent;color:" + c["text"] + "'></div><div style='margin-top:26px;display:flex;gap:12px;justify-content:center'><button style='background:" + c["chip"] + ";border:1px solid " + c["border"] + ";border-radius:6px;color:" + c["text"] + ";padding:9px 18px;font-size:14px'>Falcon Search</button><button style='background:" + c["chip"] + ";border:1px solid " + c["border"] + ";border-radius:6px;color:" + c["text"] + ";padding:9px 18px;font-size:14px'>I'm Feeling Sovereign</button></div></form>"
    html = html + "</div></body></html>"
    devolver html
  }

  def resultados(q, theme) {
    c = este.colores(theme)
    res = este.buscar(q)
    rel = este.relacionadas(q)
    ai = ia.sentimiento(q)
    otro = "dark"
    si theme == "dark" { otro = "light" }
    html = este.head(c, q + " - Falcon Search")
    html = html + "<div style='max-width:1100px;margin:0 auto;padding:0 20px'>"
    html = html + "<div style='display:flex;align-items:center;gap:16px;padding:16px 0;border-bottom:1px solid " + c["border"] + "'><a href='/?t=" + theme + "' style='font-size:28px'>🦅</a>" + este.barra(q, c, theme) + "<a href='/buscar?q=" + q + "&t=" + otro + "' style='color:" + c["link"] + ";font-size:13px'>🌙 " + otro + "</a></div>"
    html = html + "<div style='color:" + c["muted"] + ";font-size:13px;margin:14px 0 22px'>" + texto(len(res)) + " sovereign results · 3 sources · no logs · no trackers</div>"
    html = html + "<div style='display:flex;gap:36px;flex-wrap:wrap'><div style='flex:1;min-width:300px'>"
    para r en res {
      html = html + "<div style='margin-bottom:28px;max-width:620px'><div style='color:" + c["url"] + ";font-size:13px'>" + r["url"] + "<span style='display:inline-block;background:" + c["chip"] + ";border-radius:12px;padding:2px 10px;font-size:12px;color:" + c["muted"] + ";margin-left:6px'>" + r["fuente"] + "</span></div><h3 style='font-size:20px;margin:2px 0 4px'><a href='" + r["url"] + "' style='color:" + c["link"] + "'>" + r["titulo"] + "</a></h3><p style='font-size:14px;line-height:1.55;color:" + c["muted"] + "'>" + r["desc"] + "</p></div>"
    }
    html = html + "<div style='margin:20px 0'><b>Related:</b><br>"
    para t en rel {
      html = html + "<a href='/buscar?q=" + t + "&t=" + theme + "' style='display:inline-block;background:" + c["chip"] + ";border-radius:16px;padding:6px 14px;margin:4px 6px 4px 0;color:" + c["link"] + ";font-size:13px'>" + t + "</a>"
    }
    html = html + "</div></div>"
    html = html + "<div style='width:320px'><div style='border:1px solid " + c["border"] + ";border-radius:12px;padding:18px;background:" + c["card"] + "'><span style='display:inline-block;background:#f59e0b;color:#111;border-radius:12px;padding:3px 12px;font-size:12px;font-weight:bold'>🦅 SOVEREIGN AI</span><h3 style='margin:12px 0 6px'>" + q + "</h3><p style='font-size:14px;line-height:1.5'>Nexus AI insight: " + texto(ai) + "</p><hr style='margin:12px 0'><p style='font-size:13px;color:" + c["muted"] + "'>Falcon never logs your searches. Your data stays yours. Built with NexusLang.</p><p style='font-size:13px;margin-top:8px'>🔎 Total sovereign searches: " + texto(db.falcon.stats.busquedas) + "</p></div></div></div>"
    html = html + "<div style='color:" + c["muted"] + ";font-size:13px;padding:26px 0;text-align:center'>🦅 FalconSearch — See everything. Track nothing. · Powered by NexusLang</div></div></body></html>"
    devolver html
  }
}

motor = FalconSearch()
servidor = web.servidor(8080)

servidor.ruta("/", funcion(params) {
  theme = "light"
  si params["t"] == "dark" { theme = "dark" }
  devolver web.pagina(motor.home(theme))
})

servidor.ruta("/buscar", funcion(params) {
  theme = "light"
  si params["t"] == "dark" { theme = "dark" }
  db.falcon.stats.busquedas = db.falcon.stats.busquedas + 1
  devolver web.pagina(motor.resultados(params["q"], theme))
})

imprimir("✅ FalconSearch en http://localhost:8080")
EOF

python nexuslang.py falcon/falcon.nx
cat examples/web_demo.nx examples/api_demo.nx examples/juego_adivina.nx
cat examples/app_web.nx examples/demo_profesional.nx
cd ~ && mkdir -p nexusshop && cat > nexusshop/nexusshop.nx << 'EOF'
// ==========================================
// NEXUSSHOP v0.5 - El Shopify Soberano
// Multi-tienda + WhatsApp + Stats + API
// Hecho 100% con NexusLang
// ==========================================
importar web

clase NexusShop {
    def __init__() {
        este.tiendas = {}
        este.slugs = []
        este.visitas = {}
        este.admin = "542257550650"
        imprimir("🛒 NexusShop v0.5 - El Shopify Soberano")
    }

    def crear_tienda(slug, nombre, whatsapp, emoji) {
        este.tiendas[slug] = {"nombre": nombre, "whatsapp": whatsapp, "emoji": emoji, "productos": []}
        este.slugs.agregar(slug)
        este.visitas[slug] = 0
    }

    def agregar_producto(slug, nombre, precio, emoji) {
        este.tiendas[slug]["productos"].agregar({"nombre": nombre, "precio": precio, "emoji": emoji})
    }

    def tarjeta(p, whatsapp) {
        link = "https://wa.me/" + whatsapp + "?text=Hola+quiero+pedir+" + p["nombre"]
        devolver "<div style='background:white;border:1px solid lightgray;border-radius:12px;padding:18px;margin:12px 0;display:flex;justify-content:space-between;align-items:center'><div><span style='font-size:32px'>" + p["emoji"] + "</span> <b style='font-size:17px'>" + p["nombre"] + "</b><br><span style='color:seagreen;font-size:20px;font-weight:bold'>$" + texto(p["precio"]) + "</span></div><a href='" + link + "' style='background:seagreen;color:white;padding:10px 16px;border-radius:8px;text-decoration:none;font-weight:bold'>Pedir por WhatsApp</a></div>"
    }

    def vista_tienda(slug) {
        t = este.tiendas[slug]
        este.visitas[slug] = este.visitas[slug] + 1
        pedido = "Hola+quiero+pedir+"
        contenido = "<div style='max-width:900px;margin:0 auto;padding:30px 20px'>"
        contenido = contenido + "<h1>" + t["emoji"] + " " + t["nombre"] + "</h1>"
        contenido = contenido + "<p style='color:gray'>Catálogo oficial · Pedidos por WhatsApp · 👀 " + texto(este.visitas[slug]) + " visitas</p>"
        para p en t["productos"] {
            contenido = contenido + este.tarjeta(p, t["whatsapp"])
            pedido = pedido + p["nombre"] + "+"
        }
        contenido = contenido + "<div style='text-align:center;margin:20px 0'><a href='https://wa.me/" + t["whatsapp"] + "?text=" + pedido + "' style='background:black;color:white;padding:14px 26px;border-radius:8px;text-decoration:none;font-weight:bold'>🛒 Pedir TODO por WhatsApp</a></div>"
        contenido = contenido + "<p style='color:gray;font-size:13px;text-align:center'>Creada con NexusShop · Hecha con NexusLang</p></div>"
        devolver web.pagina(t["nombre"], contenido)
    }

    def landing() {
        contenido = "<div style='max-width:900px;margin:0 auto;padding:40px 20px;text-align:center'>"
        contenido = contenido + "<div style='font-size:60px'>🛒</div>"
        contenido = contenido + "<h1 style='font-size:44px'>Nexus<span style='color:seagreen'>Shop</span></h1>"
        contenido = contenido + "<p style='color:gray;font-size:18px'>Tu tienda online en minutos. Sin comisiones. Sin Big Tech.<br>Pedidos directo a tu WhatsApp.</p>"
        contenido = contenido + "<div style='margin:26px 0'><a href='/tiendas' style='background:seagreen;color:white;padding:14px 30px;border-radius:8px;font-size:16px;font-weight:bold;text-decoration:none'>Ver tiendas en vivo</a></div>"
        contenido = contenido + "<div style='display:flex;gap:14px;justify-content:center;flex-wrap:wrap'><div style='background:white;border:1px solid lightgray;border-radius:12px;padding:20px;width:220px'><b>GRATIS</b><br><span style='font-size:26px'>$0</span><br><small>10 productos · catálogo WhatsApp</small></div><div style='background:black;color:white;border-radius:12px;padding:20px;width:220px'><b>PRO</b><br><span style='font-size:26px'>$15/mes</span><br><small>ilimitados + dominio propio</small></div><div style='background:white;border:1px solid lightgray;border-radius:12px;padding:20px;width:220px'><b>ENTERPRISE</b><br><span style='font-size:26px'>$49/mes</span><br><small>multi-sucursal + API</small></div></div>"
        contenido = contenido + "<p style='color:gray;margin-top:26px'>Hecho con NexusLang — el primer lenguaje de programación bilingüe.</p></div>"
        devolver web.pagina("NexusShop - El Shopify Soberano", contenido)
    }

    def directorio() {
        contenido = "<div style='max-width:900px;margin:0 auto;padding:30px 20px'><h1>🛍️ Tiendas en vivo</h1>"
        para s en este.slugs {
            t = este.tiendas[s]
            contenido = contenido + "<a href='/tienda/" + s + "' style='display:block;background:white;border:1px solid lightgray;border-radius:12px;padding:18px;margin:12px 0;text-decoration:none;color:black'><b style='font-size:18px'>" + t["emoji"] + " " + t["nombre"] + "</b> <span style='color:gray'>· " + texto(len(t["productos"])) + " productos · " + texto(este.visitas[s]) + " visitas</span></a>"
        }
        contenido = contenido + "</div>"
        devolver web.pagina("Tiendas - NexusShop", contenido)
    }

    def datos() {
        devolver {"plataforma": "NexusShop", "tiendas": len(este.slugs), "motor": "NexusLang 5.3", "soberano": verdadero}
    }
}

shop = NexusShop()

// --- Tiendas sembradas (acá onboardamos clientes reales) ---
shop.crear_tienda("demo", "Tech Store Demo", "542257550650", "💻")
shop.agregar_producto("demo", "Laptop Pro", 999, "💻")
shop.agregar_producto("demo", "Mouse Gamer", 29, "🖱️")
shop.agregar_producto("demo", "Teclado Mecánico", 89, "⌨️")

shop.crear_tienda("lucas", "Nexus Official Store", "542257550650", "🦅")
shop.agregar_producto("lucas", "Curso NexusLang", 49, "🎓")
shop.agregar_producto("lucas", "Licencia Pro", 99, "🔑")

shop.crear_tienda("cafe", "Café de Mar", "542257550650", "☕")
shop.agregar_producto("cafe", "Café Molido 500g", 8, "☕")
shop.agregar_producto("cafe", "Medialunas x6", 5, "🥐")

// --- Rutas ---
def inicio() => shop.landing()
def tiendas() => shop.directorio()
def v_demo() => shop.vista_tienda("demo")
def v_lucas() => shop.vista_tienda("lucas")
def v_cafe() => shop.vista_tienda("cafe")
def api() => shop.datos()

s = web.servidor(8080)
s.ruta("/", inicio)
s.ruta("/tiendas", tiendas)
s.ruta("/tienda/demo", v_demo)
s.ruta("/tienda/lucas", v_lucas)
s.ruta("/tienda/cafe", v_cafe)
s.ruta("/api", api)
imprimir("✅ NexusShop en http://localhost:8080")
s.iniciar()
EOF

python nexuslang.py nexusshop/nexusshop.nx
cd ~ && cat > nexusshop/nexusshop.nx << 'EOF'

// NexusShop v0.6 - El Shopify Soberano
clase NexusShop {
    def __init__() {
        este.tiendas = {}
        este.slugs = []
        este.visitas = {}
        este.admin = "542257550650"
        imprimir("🛒 NexusShop v0.6 - El Shopify Soberano")
    }

    def crear_tienda(slug, nombre, whatsapp, emoji) {
        este.tiendas[slug] = {"nombre": nombre, "whatsapp": whatsapp, "emoji": emoji, "productos": []}
        este.slugs.agregar(slug)
        este.visitas[slug] = 0
    }

    def agregar_producto(slug, nombre, precio, emoji) {
        este.tiendas[slug]["productos"].agregar({"nombre": nombre, "precio": precio, "emoji": emoji})
    }

    def tarjeta(p, whatsapp) {
        link = "https://wa.me/" + whatsapp + "?text=Hola+quiero+pedir+" + p["nombre"]
        devolver "<div style='background:white;border:1px solid lightgray;border-radius:12px;padding:18px;margin:12px 0;display:flex;justify-content:space-between;align-items:center'><div><span style='font-size:32px'>" + p["emoji"] + "</span> <b style='font-size:17px'>" + p["nombre"] + "</b><br><span style='color:seagreen;font-size:20px;font-weight:bold'>$" + texto(p["precio"]) + "</span></div><a href='" + link + "' style='background:seagreen;color:white;padding:10px 16px;border-radius:8px;text-decoration:none;font-weight:bold'>Pedir por WhatsApp</a></div>"
    }

    def vista_tienda(slug) {
        t = este.tiendas[slug]
        este.visitas[slug] = este.visitas[slug] + 1
        pedido = "Hola+quiero+pedir+"
        contenido = "<div style='max-width:900px;margin:0 auto;padding:30px 20px'>"
        contenido = contenido + "<h1>" + t["emoji"] + " " + t["nombre"] + "</h1>"
        contenido = contenido + "<p style='color:gray'>Catálogo oficial · Pedidos por WhatsApp · 👀 " + texto(este.visitas[slug]) + " visitas</p>"
        para p en t["productos"] {
            contenido = contenido + este.tarjeta(p, t["whatsapp"])
            pedido = pedido + p["nombre"] + "+"
        }
        contenido = contenido + "<div style='text-align:center;margin:20px 0'><a href='https://wa.me/" + t["whatsapp"] + "?text=" + pedido + "' style='background:black;color:white;padding:14px 26px;border-radius:8px;text-decoration:none;font-weight:bold'>🛒 Pedir TODO por WhatsApp</a></div>"
        contenido = contenido + "<p style='color:gray;font-size:13px;text-align:center'>Creada con NexusShop · Hecha con NexusLang</p></div>"
        devolver web.pagina(t["nombre"], contenido)
    }

    def landing() {
        contenido = "<div style='max-width:900px;margin:0 auto;padding:40px 20px;text-align:center'>"
        contenido = contenido + "<div style='font-size:60px'>🛒</div>"
        contenido = contenido + "<h1 style='font-size:44px'>Nexus<span style='color:seagreen'>Shop</span></h1>"
        contenido = contenido + "<p style='color:gray;font-size:18px'>Tu tienda online en minutos. Sin comisiones. Sin Big Tech.<br>Pedidos directo a tu WhatsApp.</p>"
        contenido = contenido + "<div style='margin:26px 0'><a href='/tiendas' style='background:seagreen;color:white;padding:14px 30px;border-radius:8px;font-size:16px;font-weight:bold;text-decoration:none'>Ver tiendas en vivo</a></div>"
        contenido = contenido + "<div style='display:flex;gap:14px;justify-content:center;flex-wrap:wrap'><div style='background:white;border:1px solid lightgray;border-radius:12px;padding:20px;width:220px'><b>GRATIS</b><br><span style='font-size:26px'>$0</span><br><small>10 productos · catálogo WhatsApp</small></div><div style='background:black;color:white;border-radius:12px;padding:20px;width:220px'><b>PRO</b><br><span style='font-size:26px'>$15/mes</span><br><small>ilimitados + dominio propio</small></div><div style='background:white;border:1px solid lightgray;border-radius:12px;padding:20px;width:220px'><b>ENTERPRISE</b><br><span style='font-size:26px'>$49/mes</span><br><small>multi-sucursal + API</small></div></div>"
        contenido = contenido + "<p style='color:gray;margin-top:26px'>Hecho con NexusLang — el primer lenguaje de programación bilingüe.</p></div>"
        devolver web.pagina("NexusShop - El Shopify Soberano", contenido)
    }

    def directorio() {
        contenido = "<div style='max-width:900px;margin:0 auto;padding:30px 20px'><h1>🛍️ Tiendas en vivo</h1>"
        para s en este.slugs {
            t = este.tiendas[s]
            contenido = contenido + "<a href='/tienda/" + s + "' style='display:block;background:white;border:1px solid lightgray;border-radius:12px;padding:18px;margin:12px 0;text-decoration:none;color:black'><b style='font-size:18px'>" + t["emoji"] + " " + t["nombre"] + "</b> <span style='color:gray'>· " + texto(len(t["productos"])) + " productos · " + texto(este.visitas[s]) + " visitas</span></a>"
        }
        contenido = contenido + "</div>"
        devolver web.pagina("Tiendas - NexusShop", contenido)
    }

    def datos() {
        devolver {"plataforma": "NexusShop", "tiendas": len(este.slugs), "motor": "NexusLang 5.3", "soberano": verdadero}
    }
}

shop = NexusShop()

// Tiendas sembradas
shop.crear_tienda("demo", "Tech Store Demo", "542257550650", "💻")
shop.agregar_producto("demo", "Laptop Pro", 999, "💻")
shop.agregar_producto("demo", "Mouse Gamer", 29, "🖱️")
shop.agregar_producto("demo", "Teclado Mecánico", 89, "⌨️")

shop.crear_tienda("lucas", "Nexus Official Store", "542257550650", "🦅")
shop.agregar_producto("lucas", "Curso NexusLang", 49, "🎓")
shop.agregar_producto("lucas", "Licencia Pro", 99, "🔑")

shop.crear_tienda("cafe", "Café de Mar", "542257550650", "☕")
shop.agregar_producto("cafe", "Café Molido 500g", 8, "☕")
shop.agregar_producto("cafe", "Medialunas x6", 5, "🥐")

// Rutas
def inicio() => shop.landing()
def tiendas() => shop.directorio()
def v_demo() => shop.vista_tienda("demo")
def v_lucas() => shop.vista_tienda("lucas")
def v_cafe() => shop.vista_tienda("cafe")
def api() => shop.datos()

s = web.servidor(8080)
s.ruta("/", inicio)
s.ruta("/tiendas", tiendas)
s.ruta("/tienda/demo", v_demo)
s.ruta("/tienda/lucas", v_lucas)
s.ruta("/tienda/cafe", v_cafe)
s.ruta("/api", api)
imprimir("✅ NexusShop en http://localhost:8080")
s.iniciar()
EOF

head -3 nexusshop/nexusshop.nx
python nexuslang.py nexusshop/nexusshop.nx
cd ~ && cat > nexusshop/nexusshop.nx << 'EOF'

// NexusShop v0.7 - El Shopify Soberano
clase NexusShop {
    def __init__() {
        este.tiendas = {}
        este.slugs = []
        este.visitas = {}
        este.admin = "542257550650"
        imprimir("🛒 NexusShop v0.7 - El Shopify Soberano")
    }

    def crear_tienda(slug, nombre, whatsapp, emoji) {
        este.tiendas[slug] = {"nombre": nombre, "whatsapp": whatsapp, "emoji": emoji, "productos": []}
        este.slugs = este.slugs + [slug]
        este.visitas[slug] = 0
    }

    def agregar_producto(slug, nombre, precio, emoji) {
        este.tiendas[slug]["productos"] = este.tiendas[slug]["productos"] + [{"nombre": nombre, "precio": precio, "emoji": emoji}]
    }

    def tarjeta(p, whatsapp) {
        link = "https://wa.me/" + whatsapp + "?text=Hola+quiero+pedir+" + p["nombre"]
        devolver "<div style='background:white;border:1px solid lightgray;border-radius:12px;padding:18px;margin:12px 0;display:flex;justify-content:space-between;align-items:center'><div><span style='font-size:32px'>" + p["emoji"] + "</span> <b style='font-size:17px'>" + p["nombre"] + "</b><br><span style='color:seagreen;font-size:20px;font-weight:bold'>$" + texto(p["precio"]) + "</span></div><a href='" + link + "' style='background:seagreen;color:white;padding:10px 16px;border-radius:8px;text-decoration:none;font-weight:bold'>Pedir por WhatsApp</a></div>"
    }

    def vista_tienda(slug) {
        t = este.tiendas[slug]
        este.visitas[slug] = este.visitas[slug] + 1
        pedido = "Hola+quiero+pedir+"
        contenido = "<div style='max-width:900px;margin:0 auto;padding:30px 20px'>"
        contenido = contenido + "<h1>" + t["emoji"] + " " + t["nombre"] + "</h1>"
        contenido = contenido + "<p style='color:gray'>Catálogo oficial · Pedidos por WhatsApp · 👀 " + texto(este.visitas[slug]) + " visitas</p>"
        para p en t["productos"] {
            contenido = contenido + este.tarjeta(p, t["whatsapp"])
            pedido = pedido + p["nombre"] + "+"
        }
        contenido = contenido + "<div style='text-align:center;margin:20px 0'><a href='https://wa.me/" + t["whatsapp"] + "?text=" + pedido + "' style='background:black;color:white;padding:14px 26px;border-radius:8px;text-decoration:none;font-weight:bold'>🛒 Pedir TODO por WhatsApp</a></div>"
        contenido = contenido + "<p style='color:gray;font-size:13px;text-align:center'>Creada con NexusShop · Hecha con NexusLang</p></div>"
        devolver web.pagina(t["nombre"], contenido)
    }

    def landing() {
        contenido = "<div style='max-width:900px;margin:0 auto;padding:40px 20px;text-align:center'>"
        contenido = contenido + "<div style='font-size:60px'>🛒</div>"
        contenido = contenido + "<h1 style='font-size:44px'>Nexus<span style='color:seagreen'>Shop</span></h1>"
        contenido = contenido + "<p style='color:gray;font-size:18px'>Tu tienda online en minutos. Sin comisiones. Sin Big Tech.<br>Pedidos directo a tu WhatsApp.</p>"
        contenido = contenido + "<div style='margin:26px 0'><a href='/tiendas' style='background:seagreen;color:white;padding:14px 30px;border-radius:8px;font-size:16px;font-weight:bold;text-decoration:none'>Ver tiendas en vivo</a></div>"
        contenido = contenido + "<div style='display:flex;gap:14px;justify-content:center;flex-wrap:wrap'><div style='background:white;border:1px solid lightgray;border-radius:12px;padding:20px;width:220px'><b>GRATIS</b><br><span style='font-size:26px'>$0</span><br><small>10 productos · catálogo WhatsApp</small></div><div style='background:black;color:white;border-radius:12px;padding:20px;width:220px'><b>PRO</b><br><span style='font-size:26px'>$15/mes</span><br><small>ilimitados + dominio propio</small></div><div style='background:white;border:1px solid lightgray;border-radius:12px;padding:20px;width:220px'><b>ENTERPRISE</b><br><span style='font-size:26px'>$49/mes</span><br><small>multi-sucursal + API</small></div></div>"
        contenido = contenido + "<p style='color:gray;margin-top:26px'>Hecho con NexusLang — el primer lenguaje de programación bilingüe.</p></div>"
        devolver web.pagina("NexusShop - El Shopify Soberano", contenido)
    }

    def directorio() {
        contenido = "<div style='max-width:900px;margin:0 auto;padding:30px 20px'><h1>🛍️ Tiendas en vivo</h1>"
        para s en este.slugs {
            t = este.tiendas[s]
            contenido = contenido + "<a href='/tienda/" + s + "' style='display:block;background:white;border:1px solid lightgray;border-radius:12px;padding:18px;margin:12px 0;text-decoration:none;color:black'><b style='font-size:18px'>" + t["emoji"] + " " + t["nombre"] + "</b> <span style='color:gray'>· " + texto(len(t["productos"])) + " productos · " + texto(este.visitas[s]) + " visitas</span></a>"
        }
        contenido = contenido + "</div>"
        devolver web.pagina("Tiendas - NexusShop", contenido)
    }

    def datos() {
        devolver {"plataforma": "NexusShop", "tiendas": len(este.slugs), "motor": "NexusLang 5.3", "soberano": verdadero}
    }
}

shop = NexusShop()

// Tiendas sembradas
shop.crear_tienda("demo", "Tech Store Demo", "542257550650", "💻")
shop.agregar_producto("demo", "Laptop Pro", 999, "💻")
shop.agregar_producto("demo", "Mouse Gamer", 29, "🖱️")
shop.agregar_producto("demo", "Teclado Mecánico", 89, "⌨️")

shop.crear_tienda("lucas", "Nexus Official Store", "542257550650", "🦅")
shop.agregar_producto("lucas", "Curso NexusLang", 49, "🎓")
shop.agregar_producto("lucas", "Licencia Pro", 99, "🔑")

shop.crear_tienda("cafe", "Café de Mar", "542257550650", "☕")
shop.agregar_producto("cafe", "Café Molido 500g", 8, "☕")
shop.agregar_producto("cafe", "Medialunas x6", 5, "🥐")

// Rutas
def inicio() => shop.landing()
def tiendas() => shop.directorio()
def v_demo() => shop.vista_tienda("demo")
def v_lucas() => shop.vista_tienda("lucas")
def v_cafe() => shop.vista_tienda("cafe")
def api() => shop.datos()

s = web.servidor(8080)
s.ruta("/", inicio)
s.ruta("/tiendas", tiendas)
s.ruta("/tienda/demo", v_demo)
s.ruta("/tienda/lucas", v_lucas)
s.ruta("/tienda/cafe", v_cafe)
s.ruta("/api", api)
imprimir("✅ NexusShop en http://localhost:8080")
s.iniciar()
EOF

python nexuslang.py nexusshop/nexusshop.nx
sed -i 's/8080/8081/g' nexusshop/nexusshop.nx
python nexuslang.py nexusshop/nexusshop.nx
sed -i 's/8081/8082/g' nexusshop/nexusshop.nx
python nexuslang.py nexusshop/nexusshop.nx
