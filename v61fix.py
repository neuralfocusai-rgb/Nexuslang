src = open('nexuslang.py').read()
old = """            if tq:
                in_triple = tq
                py.append(raw)
                continue"""
new = """            if tq:
                in_triple = tq"""
print('fix ->', src.count(old))
src = src.replace(old, new, 1)
open('nexuslang.py','w').write(src)
print('FIX OK')
