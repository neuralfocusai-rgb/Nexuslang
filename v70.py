import re
src = open('nexuslang.py').read()
def rep(old, new, tag):
    global src
    n = src.count(old)
    print(tag, '->', n)
    if n == 1: src = src.replace(old, new, 1)

rep('class DBPath:', '''import json as _json
import os as _os
_NEXUS_DB_FILE = _os.environ.get('NEXUS_DB', 'nexus_data.json')
def _db_load():
    if _os.path.exists(_NEXUS_DB_FILE):
        try:
            return _json.load(open(_NEXUS_DB_FILE, encoding='utf-8'))
        except Exception:
            return {}
    return {}
def _db_flush(data):
    try:
        _json.dump(data, open(_NEXUS_DB_FILE, 'w', encoding='utf-8'), ensure_ascii=False)
    except Exception:
        pass
class DBPath:''', 'db_io')

rep("""            else:
                if not isinstance(actual.get(parte), dict): actual[parte] = {}
                actual = actual[parte]""", """            else:
                if not isinstance(actual.get(parte), dict): actual[parte] = {}
                actual = actual[parte]
        _db_flush(self._data)""", 'flush')

m = re.search(r'(\w+) = DBPath\(\{\}, \[\]\)', src)
if m:
    src = src.replace(m.group(0), m.group(1) + ' = DBPath(_db_load(), [])', 1)
    print('instancia ->', m.group(0))
else:
    print('ERROR instancia; candidatas:')
    for i, l in enumerate(src.split('\n')):
        if 'DBPath(' in l and 'self' not in l: print(i+1, l)

rep('VERSION = "6.3.0"', 'VERSION = "7.0.0"', 'version')
open('nexuslang.py','w').write(src)
print('MOTOR v7.0 OK')

src = open('nexusshop/v20.nx').read()
old = """    def __init__() {
        este.tiendas = {}
        este.slugs = []"""
new = """    def __init__() {
        este.tiendas = db.nexusshop.tiendas
        si este.tiendas == None {
            este.tiendas = {}
        }
        este.slugs = db.nexusshop.slugs
        si este.slugs == None {
            este.slugs = []
        }"""
print('init_carga ->', src.count(old))
src = src.replace(old, new, 1)
open('nexusshop/v20.nx','w').write(src)
print('MARKETPLACE v7.0 OK')
