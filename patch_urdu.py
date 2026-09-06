src = open('nexuslang.py', encoding='utf-8').read()
marker = '# --- URDU v6.4 ---'
add = """
    # --- URDU v10.0 (nativo y completo) ---
    (r'\\bفنکشن\\b', 'def'), (r'\\bلکھو\\b', 'print'), (r'\\bپڑھو\\b', 'input'),
    (r'\\bدرآمد\\b', 'import'), (r'\\bمتغیر\\s+', ''), (r'\\bکلاس\\b', 'class'),
"""
if marker in src:
    src = src.replace(marker, marker + add, 1)
    open('nexuslang.py','w',encoding='utf-8').write(src)
    print('Parche URDU v10.0 aplicado OK')
else:
    print('Marker no encontrado')
