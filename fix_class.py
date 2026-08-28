with open('nexuslang.py', 'r') as f:
    c = f.read()

c = c.replace(
    "'True': True, 'False': False, 'None': None}",
    "'True': True, 'False': False, 'None': None,\n            '__build_class__': __import__('builtins').__build_class__}"
)

with open('nexuslang.py', 'w') as f:
    f.write(c)

print("✅ FIX APLICADO")
