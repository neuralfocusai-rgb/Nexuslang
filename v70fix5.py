src = open('nexuslang.py').read()
def rep(old, new, tag):
    global src
    n = src.count(old)
    print(tag, '->', n)
    if n == 1: src = src.replace(old, new, 1)

rep("def __init__(self): object.__setattr__(self, '_data', {})", "def __init__(self): object.__setattr__(self, '_data', _db_load())", 'db_carga')
rep("'NEXUS_DB', 'nexus_data.json')", "'NEXUS_DB', 'nexus_db.json')", 'mismo_archivo')
open('nexuslang.py','w').write(src)
print('FIX5 OK')
