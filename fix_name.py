with open('nexuslang.py', 'r') as f:
    c = f.read()

c = c.replace(
    "self.ns = {'__builtins__': self._safe_builtins()}",
    "self.ns = {'__builtins__': self._safe_builtins(), '__name__': 'nexuslang', '__qualname__': ''}"
)

with open('nexuslang.py', 'w') as f:
    f.write(c)

print("✅ FIX APLICADO")
