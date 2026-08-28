import re
src = open('nexuslang.py').read()
print('--- líneas con DBPath( ---')
for i, l in enumerate(src.split('\n')):
    if 'DBPath(' in l and 'class DBPath' not in l: print(i+1, l.strip())
n = len(re.findall(r'DBPath\(\{\}, ?\[\]\)', src))
print('inst ->', n)
src = re.sub(r'DBPath\(\{\}, ?\[\]\)', 'DBPath(_db_load(), [])', src)
open('nexuslang.py','w').write(src)
print('FIX OK')
