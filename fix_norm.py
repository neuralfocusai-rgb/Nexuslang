src = open('nexuslang.py').read()
old = "    def iniciar(self):"
new = """    def normalizar(self):
        for _k in list(self.rutas):
            if type(_k) is not str:
                self.rutas[str(_k)] = self.rutas.pop(_k)
    def iniciar(self):"""
print('norm ->', src.count(old))
src = src.replace(old, new, 1)
open('nexuslang.py','w').write(src)
print('MOTOR OK')

src = open('nexusshop/v20.nx').read()
old = 's.iniciar()'
new = 's.normalizar()\ns.iniciar()'
print('call ->', src.count(old))
src = src.replace(old, new, 1)
old2 = '    devolver T(pagina_tienda_nueva(sl))'
new2 = '    devolver pagina_tienda_nueva(sl)'
print('raw ->', src.count(old2))
src = src.replace(old2, new2, 1)
open('nexusshop/v20.nx','w').write(src)
print('NX OK')
