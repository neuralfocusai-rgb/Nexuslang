# NexusLang v5.0

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
