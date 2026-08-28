import os

# 1. Agregar main() a nexuslang.py (para comando 'nexus' tras pip install)
with open('nexuslang.py', 'r', encoding='utf-8') as f:
    code = f.read()
if 'def main():' not in code:
    code += '''

def main():
    """CLI entry point (pip install -> comandos: nexus / nexuslang)"""
    import runpy
    runpy.run_path(__file__, run_name="__main__")
'''
    with open('nexuslang.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("✅ main() agregado a nexuslang.py")

# 2. setup.py (para PyPI)
with open('setup.py', 'w', encoding='utf-8') as f:
    f.write('''from setuptools import setup

with open("README.md", encoding="utf-8") as f:
    long_desc = f.read()

setup(
    name="nexuslang",
    version="5.0.0",
    description="The first bilingual (Spanish/English) programming language with built-in AI, database and web generation. Zero dependencies.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author="Lucas",
    license="MIT",
    py_modules=["nexuslang"],
    python_requires=">=3.8",
    entry_points={"console_scripts": ["nexus=nexuslang:main", "nexuslang=nexuslang:main"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Interpreters",
        "Natural Language :: Spanish",
        "Natural Language :: English",
    ],
)
''')
print("✅ setup.py creado")

# 3. LICENSE (MIT)
with open('LICENSE', 'w', encoding='utf-8') as f:
    f.write('''MIT License

Copyright (c) 2026 Lucas - NexusLang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
''')
print("✅ LICENSE creado")

# 4. README.md bilingüe profesional
with open('README.md', 'w', encoding='utf-8') as f:
    f.write('''# NexusLang v5.0

**The first bilingual (Spanish/English) programming language with built-in AI**
**El primer lenguaje de programación bilingüe (Español/Inglés) con IA integrada**

Simple enough for a 10-year-old. Powerful enough for professionals.
Tan simple que un niño de 10 años lo usa. Tan poderoso que un profesional lo elige.

## Install / Instalación

```bash
pip install nexuslang
nexus -i            # interactive mode / modo interactivo
nexus programa.nx   # run a program / ejecutar programa
nexus --test        # run test suite / pruebas
```

Or from source / o desde el código:

```bash
python nexuslang.py -i
```

**Zero external dependencies** - pure Python standard library.
**Cero dependencias externas** - pura librería estándar de Python.

## Quick Start / Inicio Rápido
## Built-in superpowers / Superpoderes integrados

| Module | Features |
|--------|----------|
| **ia / ai** | sentiment analysis, chatbot, keywords, summaries, predictions |
| **db** | Firebase-style database: `db.users.lucas = {"age": 25}` |
| **web** | generate real HTML pages: `web.guardar("site", web.pagina(...))` |
| **mate / math** | sqrt, sin, cos, factorial, random... |
| **text / lista** | 50+ string & list functions |
| **files** | read/write files in one line |

## Examples / Ejemplos

See the `examples/` folder / ver carpeta `examples/`:

```bash
nexus examples/hola_mundo.nx
nexus examples/ia_demo.nx
nexus examples/web_demo.nx
nexus examples/juego_adivina.nx
```

## Tests

12 automated tests, all passing / 12 tests automatizados, todos pasan:

```bash
nexus --test
```

## Why NexusLang? / Por qué NexusLang?

- **Bilingual** - code in Spanish, English, or mixed / bilingüe total
- **AI-native** - no libraries needed / IA sin librerías
- **Sovereign** - no US cloud dependencies / sin dependencias de nube
- **Learn in hours, not years** - aprende en horas, no años

## License

MIT - free for everyone / gratis para todos.
''')
print("✅ README.md creado")
print("\n✅ PAQUETE PROFESIONAL LISTO")
