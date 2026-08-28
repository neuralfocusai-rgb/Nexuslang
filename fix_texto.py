import re
with open('nexuslang.py', 'r', encoding='utf-8') as f:
    c = f.read()

c2 = re.sub(
    r"(class TextTools:\n)([ \t]+)(mayusculas)",
    r"\1\2def __call__(self, t): return str(t)\n\2\3",
    c, count=1
)
assert c2 != c, "TextTools no encontrado"

with open('nexuslang.py', 'w', encoding='utf-8') as f:
    f.write(c2)
print("✅ texto() ahora funciona como funcion Y como modulo")
