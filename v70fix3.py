src = open('nexusshop/v20.nx').read()
def rep(old, new, tag):
    global src
    n = src.count(old)
    print(tag, '->', n)
    if n == 1: src = src.replace(old, new, 1)

rep("""        este.tiendas = db.nexusshop.tiendas
        si este.tiendas == None {
            este.tiendas = {}
        }
        este.slugs = db.nexusshop.slugs
        si este.slugs == None {
            este.slugs = []
        }""", """        este.tiendas = db.nexusshop.tiendas.get()
        si este.tiendas == None {
            este.tiendas = {}
        }
        este.slugs = db.nexusshop.slugs.get()
        si este.slugs == None {
            este.slugs = []
        }""", 'get_init')

rep('s.ruta("/crear", lambda: T(pagina_crear()))', '''i = 0
mientras i < len(shop.slugs) {
    sl = shop.slugs[i]
    si sl != "nexus" {
        si sl != "demo" {
            si sl != "cafe" {
                si sl != "almacen" {
                    si sl != "boutique" {
                        si sl != "farma" {
                            s.ruta("/comprar/" + sl, lambda sl2=sl: T(pagina_tienda_nueva(sl2)))
                        }
                    }
                }
            }
        }
    }
    i = i + 1
}
s.ruta("/crear", lambda: T(pagina_crear()))''', 'rutas_persistidas')

open('nexusshop/v20.nx','w').write(src)
print('FIX3 OK')
