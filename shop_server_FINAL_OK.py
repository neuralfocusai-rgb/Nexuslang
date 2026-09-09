import json, secrets, datetime
from http.server import HTTPServer,BaseHTTPRequestHandler
from urllib.parse import urlparse,parse_qs,quote
TR={"search":{"en":"Search products...","ur":"مصنوعات تلاش کریں...","es":"Buscar productos..."},
"cod":{"en":"Cash on Delivery","ur":"کیش آن ڈیلیوری","es":"Pago contra entrega"},
"delivery":{"en":"Nationwide delivery","ur":"ملک بھر میں ترسیل","es":"Envío a todo el país"},
"order":{"en":"Order","ur":"آرڈر","es":"Pedir"},
"banner":{"en":"Mega Sale — up to 40% off","ur":"میگا سیل — 40% تک چھوٹ","es":"Mega oferta — hasta 40%"},
"live":{"en":"Live stores","ur":"فعال دکانیں","es":"Tiendas en vivo"},
"products":{"en":"products","ur":"مصنوعات","es":"productos"},
"reviews":{"en":"Reviews","ur":"جائزے","es":"Reseñas"},
"back":{"en":"Back","ur":"واپس","es":"Volver"},
"cats":{"en":"Categories","ur":"زمرے","es":"Categorías"},
"offers":{"en":"Offers","ur":"آفرز","es":"Ofertas"},
"home":{"en":"Home","ur":"ہوم","es":"Inicio"},
"stores":{"en":"Stores","ur":"دکانیں","es":"Tiendas"},
"results":{"en":"results","ur":"نتائج","es":"resultados"},
"noresults":{"en":"No results","ur":"کوئی نتیجہ نہیں","es":"Sin resultados"},
"addcart":{"en":"Add to cart","ur":"کارٹ میں ڈالیں","es":"Agregar al carrito"},
"cart":{"en":"Cart","ur":"کارٹ","es":"Carrito"},
"checkout":{"en":"Checkout via WhatsApp","ur":"واٹس ایپ پر چیک آؤٹ","es":"Pedir por WhatsApp"},
"empty":{"en":"Cart is empty","ur":"کارٹ خالی ہے","es":"Carrito vacío"},
"made":{"en":"Built with NexusShop · Made with NexusLang","ur":"NexusShop سے بنا · NexusLang سے تیار","es":"Creado con NexusShop · Hecho con NexusLang"}}
CSS="""*{box-sizing:border-box;margin:0;padding:0}html,body{max-width:100%;overflow-x:hidden}
body{font-family:system-ui,sans-serif;background:#f5f5f5;color:#111;padding-bottom:70px}
header{position:sticky;top:0;background:#0b6b3a;color:#fff;padding:10px 16px;z-index:9}
.row1{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.logo{font-weight:800;font-size:20px}.lang a{color:#fff;text-decoration:none;margin-inline-start:8px;font-size:13px}
.searchform{display:flex}.searchform input{flex:1;min-width:0;border:0;border-radius:8px;padding:10px 14px;font-size:14px}
.searchform button{border:0;background:#ffd166;border-radius:8px;padding:0 14px;font-size:16px}
.banner{background:linear-gradient(135deg,#0b6b3a,#129152);color:#fff;border-radius:14px;padding:24px 16px;margin:16px;text-align:center;font-size:19px;font-weight:800}
.trust{display:flex;justify-content:space-around;background:#fff;padding:12px;margin:0 16px 14px;border-radius:12px;font-size:11px;text-align:center;gap:6px}
.chips{display:flex;gap:8px;overflow-x:auto;padding:0 16px 12px}.chip{background:#fff;border:1px solid #e0e0e0;border-radius:20px;padding:8px 16px;white-space:nowrap;font-size:13px;text-decoration:none;color:#111}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;padding:0 16px}
.pcard{background:#fff;border-radius:12px;overflow:hidden;position:relative;min-width:0;text-decoration:none;color:inherit;display:block}
.pimg{background:#f0f0f0;font-size:52px;text-align:center;padding:24px 0}
.pinfo{padding:10px}.pname{font-size:14px;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.stars{color:#f85606;font-size:12px}.price{font-size:16px;font-weight:800;color:#0b6b3a}
.badge{position:absolute;top:8px;inset-inline-start:8px;background:#f85606;color:#fff;font-size:11px;font-weight:700;border-radius:6px;padding:3px 8px}
.order,.add{display:block;text-align:center;background:#25D366;color:#fff;padding:10px;border-radius:8px;font-weight:700;text-decoration:none;margin-top:8px;font-size:14px;border:0;width:100%;cursor:pointer}
.add{background:#0b6b3a}
.store{color:#777;font-size:12px}
.foot{color:#999;font-size:12px;text-align:center;padding:24px}h2{margin:16px}
.detail{background:#fff;margin:16px;border-radius:14px;padding:20px}
.dimg{font-size:90px;text-align:center;padding:20px 0}
.bottomnav{position:fixed;bottom:0;left:0;right:0;background:#fff;display:flex;justify-content:space-around;padding:8px 0;border-top:1px solid #eee;z-index:9}
.bottomnav a{text-decoration:none;color:#777;font-size:11px;text-align:center}
.cartbtn{position:fixed;bottom:64px;inset-inline-end:16px;background:#0b6b3a;color:#fff;border-radius:50%;width:54px;height:54px;font-size:22px;display:flex;align-items:center;justify-content:center;z-index:10;border:0;cursor:pointer}
.cartcount{position:absolute;top:-4px;inset-inline-end:-4px;background:#f85606;color:#fff;border-radius:10px;font-size:11px;padding:2px 7px}
.drawer{position:fixed;bottom:0;left:0;right:0;background:#fff;border-radius:16px 16px 0 0;padding:20px;z-index:11;display:none;max-height:70%;overflow:auto;box-shadow:0 -4px 20px rgba(0,0,0,.2)}"""
DEMO={"lucas":{"nombre":"Mate & Co","whatsapp":"5491100000000","emoji":"🧉","resenas":[{"estrellas":5,"comentario":"Excelente!"}],
"productos":[{"nombre":"Mate Imperial","precio":15000,"emoji":"🧉","categoria":"Home","desc":"Mate premium calabaza."},{"nombre":"Bombilla Acero","precio":4000,"emoji":"🥄","categoria":"Home","desc":"Acero inoxidable."}]},
"cafe":{"nombre":"Café Lahore","whatsapp":"923000000000","emoji":"☕","resenas":[{"estrellas":4,"comentario":"Great chai"}],
"productos":[{"nombre":"Chai Latte","precio":1200,"emoji":"☕","categoria":"Food","desc":"Doodh patti style."},{"nombre":"Samosa","precio":300,"emoji":"🥟","categoria":"Food","desc":"Crispy aloo samosa."}]}}
def load():
    try:
        d=json.load(open('nexus_db.json',encoding='utf-8'))
        if isinstance(d,dict):
            if 'tiendas' in d: return d['tiendas']
            if 'nexusshop' in d: return d['nexusshop'].get('tiendas',DEMO)
    except Exception: pass
    return DEMO
TIENDAS=load()
def allp():
    return [(s,ti,p,i) for s,ti in TIENDAS.items() for i,p in enumerate(ti.get("productos",[]))]
def cats():
    c=sorted({p.get("categoria","General") for _,_,p,_ in allp()}); return c or ["General"]
def nav(l):
    t=lambda k:TR[k][l]
    return f'<div class="bottomnav"><a href="/?lang={l}">🏠<br>{t("home")}</a><a href="/categorias?lang={l}">🗂️<br>{t("cats")}</a><a href="/ofertas?lang={l}">🏷️<br>{t("offers")}</a><a href="/?lang={l}#stores">🛍️<br>{t("stores")}</a></div>'
def top(l):
    d="rtl" if l=="ur" else "ltr"; t=lambda k:TR[k][l]
    return f'<html dir="{d}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>{CSS}</style></head><body><header><div class="row1"><span class="logo">Nexus<span style="color:#ffd166">Shop</span></span><span class="lang"><a href="?lang=en">EN</a><a href="?lang=ur">اردو</a><a href="?lang=es">ES</a></span></div><form class="searchform" action="/buscar"><input name="q" placeholder="{t("search")}"><input type="hidden" name="lang" value="{l}"><button>🔍</button></form></header>'
def cartjs(l):
    t=lambda k:TR[k][l]
    return f'''<button class="cartbtn" onclick="openCart()">🛒<span class="cartcount" id="cc">0</span></button>
<div class="drawer" id="drawer"><h2>🛒 {t("cart")}</h2><div id="items"></div><button class="order" onclick="checkout()">{t("checkout")}</button><button class="add" onclick="closeCart()">{t("back")}</button></div>
<script>
function gc(){{return JSON.parse(localStorage.getItem('cart')||'{{}}')}}
function sc(c){{localStorage.setItem('cart',JSON.stringify(c));upd()}}
function upd(){{var c=gc(),n=0;for(k in c)n+=c[k].q;document.getElementById('cc').textContent=n}}
function add(id,n,p,w){{var c=gc();c[id]=c[id]||{{n:n,p:p,q:0,w:w}};c[id].q++;sc(c)}}
function openCart(){{var c=gc(),h='';for(k in c)h+='<p>'+c[k].q+'x '+c[k].n+' — Rs.'+(c[k].p*c[k].q)+'</p>';document.getElementById('items').innerHTML=h||'<p>{t("empty")}</p>';document.getElementById('drawer').style.display='block'}}
function closeCart(){{document.getElementById('drawer').style.display='none'}}
function checkout(){{var c=gc();var ks=Object.keys(c||{{}});if(!ks.length){{alert("Cart empty");return;}}var items=ks.map(function(k){{var it=c[k];return {{k:k,n:it.n,p:it.p,q:it.q,w:it.w}};}});fetch("/api/order",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{items:items}})}}).then(function(r){{return r.json()}}).then(function(j){{location.href="/pay/"+j.id}})}}
upd()</script>'''
def pcard(s,ti,p,i,l,badge=None):
    t=lambda k:TR[k][l]; b=f'<span class="badge">{badge}</span>' if badge else ''
    return f'<a class="pcard" href="/p/{s}/{i}?lang={l}">{b}<div class="pimg">{p.get("emoji","🛍️")}</div><div class="pinfo"><div class="pname">{p["nombre"]}</div><div class="store">{ti.get("emoji","")} {ti["nombre"]}</div><div class="price">Rs. {p["precio"]}</div></div></a>'
def home(l):
    t=lambda k:TR[k][l]
    chips="".join(f'<a class="chip" href="/categoria/{quote(c)}?lang={l}">{c}</a>' for c in cats())
    stores="".join(f'<a class="pcard" href="/tienda/{s}?lang={l}"><div class="pimg">{ti.get("emoji","🛍️")}</div><div class="pinfo"><div class="pname">{ti["nombre"]}</div><div class="store">{len(ti.get("productos",[]))} {t("products")}</div></div></a>' for s,ti in TIENDAS.items())
    off="".join(pcard(s,ti,p,i,l) for s,ti,p,i in allp()[:4])
    return top(l)+f'<div class="banner">🎉 {t("banner")}</div><div class="trust"><span>💵 {t("cod")}</span><span>🚚 {t("delivery")}</span></div><div class="chips">{chips}</div><h2 id="stores">{t("live")}</h2><div class="grid">{stores}</div><h2>⭐ {t("offers")}</h2><div class="grid">{off}</div><p class="foot">{t("made")}</p>{cartjs(l)}{nav(l)}</body></html>'
def detail(s,i,l):
    t=lambda k:TR[k][l]; ti=TIENDAS.get(s)
    if not ti: return home(l)
    p=ti["productos"][int(i)]
    rev="".join(f'<p class="stars">{"★"*r.get("estrellas",5)} <span class="store">{r.get("comentario","")}</span></p>' for r in ti.get("resenas",[]))
    return top(l)+f'<div class="detail"><div class="dimg">{p.get("emoji","🛍️")}</div><h2>{p["nombre"]}</h2><div class="price">Rs. {p["precio"]}</div><p class="store">{ti.get("emoji","")} {ti["nombre"]}</p><p style="margin:12px 0;color:#555">{p.get("desc","")}</p><button class="add" onclick="add(\'{s}{i}\',\'{p["nombre"]}\',{p["precio"]},\'{ti["whatsapp"]}\')">{t("addcart")}</button><a class="order" href="https://wa.me/{ti["whatsapp"]}?text={quote("Hola quiero pedir "+p["nombre"])}">🟢 {t("order")}</a><h2 style="margin-top:16px">⭐ {t("reviews")}</h2>{rev or "<p class=store>—</p>"}</div><p class="foot"><a href="/?lang={l}" style="color:#0b6b3a">← {t("back")}</a></p>{cartjs(l)}{nav(l)}</body></html>'
def categoria(c,l):
    t=lambda k:TR[k][l]
    items=[(s,ti,p,i) for s,ti,p,i in allp() if p.get("categoria","General")==c]
    g="".join(pcard(s,ti,p,i,l) for s,ti,p,i in items) or f'<p class="foot">{t("noresults")}</p>'
    return top(l)+f'<h2>🗂️ {c}</h2><div class="grid">{g}</div>{cartjs(l)}{nav(l)}</body></html>'
def catshome(l):
    t=lambda k:TR[k][l]
    chips="".join(f'<a class="chip" href="/categoria/{quote(c)}?lang={l}">{c}</a>' for c in cats())
    return top(l)+f'<h2>🗂️ {t("cats")}</h2><div class="chips">{chips}</div>{nav(l)}</body></html>'
def ofertas(l):
    t=lambda k:TR[k][l]
    g="".join(pcard(s,ti,p,i,l,badge=t("offers")) for s,ti,p,i in allp())
    return top(l)+f'<h2>🏷️ {t("offers")}</h2><div class="grid">{g}</div>{cartjs(l)}{nav(l)}</body></html>'
def buscar(q,l):
    t=lambda k:TR[k][l]
    items=[(s,ti,p,i) for s,ti,p,i in allp() if q.lower() in p["nombre"].lower()]
    g="".join(pcard(s,ti,p,i,l) for s,ti,p,i in items) or f'<p class="foot">{t("noresults")}</p>'
    return top(l)+f'<h2>🔍 {len(items)} {t("results")}</h2><div class="grid">{g}</div>{cartjs(l)}{nav(l)}</body></html>'
def store(s,l):
    t=lambda k:TR[k][l]; ti=TIENDAS.get(s)
    if not ti: return home(l)
    g="".join(pcard(s,ti,p,i,l) for i,p in enumerate(ti["productos"]))
    return top(l)+f'<h2>{ti.get("emoji","")} {ti["nombre"]}</h2><div class="grid">{g}</div>{cartjs(l)}{nav(l)}</body></html>'
ORDERS_FILE = "orders.json"
PAY = {"paypal": "nexusshopdemo", "paddle": "https://checkout.paddle.com/TU_PRICE_ID", "mp": "https://mpago.la/TU_LINK", "bank": "Wise / Payoneer: details on confirmation"}

def orders_load():
    try:
        import json as _j
        return _j.load(open(ORDERS_FILE, encoding="utf-8"))
    except Exception:
        return {}

def orders_save(d):
    import json as _j
    _j.dump(d, open(ORDERS_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def order_total(items):
    t = 0
    for it in items:
        t += int(it.get("p", 0)) * int(it.get("q", 1))
    return t

def pay_html(oid, o):
    from urllib.parse import quote
    items = o.get("items", [])
    rows = ""
    stores = {}
    for it in items:
        n = it.get("n", "Item"); q = int(it.get("q", 1)); p = int(it.get("p", 0)); w = it.get("w", "")
        rows += f"<tr><td>{n}</td><td class='c'>{q}</td><td class='r'>Rs. {p*q:,}</td></tr>"
        stores.setdefault(w, []).append(f"{q}x {n} - Rs. {p*q}")
    wa_btns = ""
    for w, ln in stores.items():
        txt = quote("Pedido NexusShop " + oid + "\n" + "\n".join(ln) + f"\nTotal: Rs. {o['total']:,}\nEstado: pendiente de verificacion")
        wa_btns += f"<a class='btn wa' target='_blank' href='https://wa.me/{w}?text={txt}'>📲 Enviar pedido por WhatsApp (+{w})</a>"
    return f"""<!DOCTYPE html><html lang='es'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Pago {oid} - NexusShop</title>
<style>body{{font-family:system-ui,sans-serif;margin:0;background:#f2f4f3;color:#111}}header{{background:#0b6b3a;color:#fff;padding:14px 16px;display:flex;justify-content:space-between;align-items:center}}header b{{font-size:18px}}main{{max-width:560px;margin:0 auto;padding:16px}}.card{{background:#fff;border-radius:14px;padding:16px;margin:0 0 14px;box-shadow:0 1px 4px rgba(0,0,0,.08)}}table{{width:100%;border-collapse:collapse;font-size:14px}}td{{padding:8px 4px;border-bottom:1px solid #eee}}.c{{text-align:center}}.r{{text-align:right}}.total{{font-size:18px;font-weight:800;text-align:right;padding-top:10px}}.btn{{display:block;width:100%;box-sizing:border-box;padding:14px;margin:8px 0;border:0;border-radius:12px;background:#0b6b3a;color:#fff;font-size:15px;font-weight:700;text-align:center;text-decoration:none}}.wa{{background:#25d366}}.alt{{background:#fff;color:#0b6b3a;border:2px solid #0b6b3a}}.badge{{display:inline-block;background:#fff3cd;color:#856404;border-radius:8px;padding:4px 10px;font-size:12px;font-weight:700;margin-right:6px}}</style></head>
<body><header><b>🛍️ NexusShop</b><span>🔒 Pago seguro</span></header><main>
<div class='card'><span class='badge'>Pedido {oid}</span><span class='badge'>{o['ts']}</span>
<table>{rows}</table><div class='total'>Total: Rs. {o['total']:,}</div></div>
<div class='card'><b>1️⃣ Elegi como pagar</b>
<a class='btn' target='_blank' href='https://paypal.me/{PAY['paypal']}'>PayPal</a>
<a class='btn' target='_blank' href='{PAY['paddle']}'>💳 Tarjeta / Apple Pay / Google Pay</a>
<a class='btn' target='_blank' href='{PAY['mp']}'>Mercado Pago</a>
<a class='btn alt' href='#wa'>💵 Transferencia / Contra entrega</a></div>
<div class='card' id='wa'><b>2️⃣ Confirma al comerciante</b>
{wa_btns}
<button class='btn' onclick="fetch('/api/pay/{oid}',{{method:'POST'}}).then(function(){{alert('✅ Gracias / Thank you / شکریہ - el comerciante verificara tu pago')}})">✅ Ya pague</button>
<div class='card'>Ref transferencia: <b>{oid}</b><br>{PAY['bank']}</div></div>
</main></body></html>"""

class H(BaseHTTPRequestHandler):
    def do_POST(self):
        ln = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(ln) if ln else b"{}"
        import json as _j
        try:
            d = _j.loads(body.decode("utf-8"))
        except Exception:
            d = {}
        if self.path == "/api/order":
            items = d.get("items", [])
            oid = "NS-" + secrets.token_hex(4).upper()
            ap = allp()
            wa = "923000000000"
            try:
                wa = items[0].get("w", wa)
            except Exception:
                pass
            o = {"id": oid, "items": items, "total": order_total(items), "wa": wa, "status": "pending_payment", "ts": datetime.date.today().isoformat()}
            od = orders_load(); od[oid] = o; orders_save(od)
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(_j.dumps({"id": oid}).encode())
        elif self.path.startswith("/api/pay/"):
            oid = self.path.split("/")[-1]
            od = orders_load()
            if oid in od:
                od[oid]["status"] = "paid_pending_verification"; orders_save(od)
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(b'{"ok":1}')
        else:
            self.send_response(404); self.end_headers()

    def paypage(self, oid):
        od = orders_load()
        o = od.get(oid)
        html = pay_html(oid, o) if o else "<h1>Order not found</h1>"
        self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers(); self.wfile.write(html.encode("utf-8"))
    def do_GET(self):
        u=urlparse(self.path); q=parse_qs(u.query); l=q.get('lang',['en'])[0]
        if u.path.startswith('/pay/'):
            return self.paypage(u.path.split('/')[2])
        if u.path.startswith('/p/'):
            parts=u.path[3:].split('/'); b=detail(parts[0],parts[1],l)
        elif u.path.startswith('/tienda/'): b=store(u.path[8:],l)
        elif u.path.startswith('/categoria/'): b=categoria(u.path[11:],l)
        elif u.path.startswith('/categorias'): b=catshome(l)
        elif u.path.startswith('/ofertas'): b=ofertas(l)
        elif u.path.startswith('/buscar'): b=buscar(q.get('q',[''])[0],l)
        else: b=home(l)
        self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8'); self.end_headers(); self.wfile.write(b.encode('utf-8'))
    def log_message(self,*a): pass
print("✅ NexusShop v4 en http://localhost:8083")
HTTPServer(('0.0.0.0',8083),H).serve_forever()
