src = open('nexusshop/v20.nx').read()
old = """        este.tiendas = db.nexusshop.tiendas.get()
        si este.tiendas == None {
            este.tiendas = {}
        }
        este.slugs = db.nexusshop.slugs.get()
        si este.slugs == None {
            este.slugs = []
        }"""
new = """        cargado = db.nexusshop.tiendas.get()
        si cargado == None {
            este.tiendas = {}
        }
        si cargado != None {
            este.tiendas = dict(cargado)
        }
        cargado_s = db.nexusshop.slugs.get()
        si cargado_s == None {
            este.slugs = []
        }
        si cargado_s != None {
            este.slugs = list(cargado_s)
        }"""
print('dict_list ->', src.count(old))
src = src.replace(old, new, 1)
open('nexusshop/v20.nx','w').write(src)
print('FINAL OK')
