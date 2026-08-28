src = open('nexuslang.py').read()
idx = src.find('class DB:')
j = src.find('self._data = {}', idx)
print('pos ->', idx, j)
if idx != -1 and j != -1 and j - idx < 400:
    src = src[:j] + 'self._data = _db_load()' + src[j+len('self._data = {}'):]
    print('FIX4 aplicado')
else:
    print('ERROR: no encontrado')
open('nexuslang.py','w').write(src)
