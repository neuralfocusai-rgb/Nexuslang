src = open('nexuslang.py').read()
old = "  (r'&&', ' and '), (r'\\|\\|', ' or '),\n]"
new = """  (r'&&', ' and '), (r'\\|\\|', ' or '),
  # --- URDU v6.4 ---
  (r'\\bورنہ\\b', ' else '), (r'\\bاگر\\b', ' if '), (r'\\bجب تک\\b', ' while '),
  (r'\\bہر\\b', ' for '), (r'\\bمیں\\b', ' in '), (r'\\bواپس\\b', ' return '),
  (r'\\bفعل\\b', ' def '), (r'\\bکلاس\\b', ' class '), (r'\\bتوڑو\\b', ' break '),
  (r'\\bجاری\\b', ' continue '), (r'\\bکوشش\\b', ' try '), (r'\\bپکڑو\\b', ' except '),
  (r'\\bآخر میں\\b', ' finally '), (r'\\bدرست\\b', ' True '), (r'\\bغلط\\b', ' False '),
  (r'\\bخالی\\b', ' None '), (r'\\bدکھاؤ\\b', ' print '), (r'\\bاور\\b', ' and '),
  (r'\\bیا\\b', ' or '), (r'\\bنہیں\\b', ' not '),
]"""
print('urdu ->', src.count(old))
src = src.replace(old, new, 1)
open('nexuslang.py','w').write(src)
print('MOTOR URDU OK')
