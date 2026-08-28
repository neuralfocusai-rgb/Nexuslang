src = open('nexuslang.py').read()
old = """    def __init__(self, data, path):
        object.__setattr__(self, '_data', data)
        object.__setattr__(self, '_path', path)"""
new = """    def __init__(self, data, path):
        if not path:
            data = _db_load() or data
        object.__setattr__(self, '_data', data)
        object.__setattr__(self, '_path', path)"""
print('init ->', src.count(old))
src = src.replace(old, new, 1)
open('nexuslang.py','w').write(src)
print('FIX2 OK')
