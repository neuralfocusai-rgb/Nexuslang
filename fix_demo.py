demo_code = open('demo_builtin.nx', encoding='utf-8').read()
block = 'DEMO_CODE = """\n' + demo_code + '"""\n\n'
with open('nexuslang.py', 'r', encoding='utf-8') as f:
    c = f.read()
if 'DEMO_CODE' not in c:
    c = c.replace('# ==================== TESTS', block + '# ==================== TESTS', 1)
old = 'if __name__ == "__main__":'
new = 'if __name__ == "__main__":\n    if len(sys.argv) > 1 and sys.argv[1] == \'--demo\':\n        NexusLang().ejecutar(DEMO_CODE)\n        sys.exit(0)'
if '--demo' not in c:
    c = c.replace(old, new, 1)
with open('nexuslang.py', 'w', encoding='utf-8') as f:
    f.write(c)
print("✅ --demo agregado" if '--demo' in open('nexuslang.py').read() else "⚠️ revisar")
