src = open('nexuslang.py').read()
old = "                serv._query = {}\n                ruta = s.path"
new = "                serv._query = {}\n                ruta = s.path\n                print(\"REQ:\", repr(ruta), \"in:\", ruta in rutas, \"fb:\", hasattr(serv, 'fallback'))"
print('dbg4 ->', src.count(old))
src = src.replace(old, new, 1)
open('nexuslang.py','w').write(src)
print('OK')
