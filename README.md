# NexusLang v9.4

The first trilingual programming language
(Spanish / English / Urdu) with native Urdu script (RTL),
its own compiler pipeline and its own virtual machine.

El primer lenguaje trilingüe (Español / Inglés / Urdu)
con escritura urdu nativa (RTL), compilador propio y
máquina virtual propia.

Simple enough for a 10-year-old. Powerful enough for
professionals.

## What's new since v5

- v6: native Urdu keywords + RTL script
- v8: compiler pipeline (lexer, parser, AST),
  bytecode (.nxb) and NexusVM
- v9: NexusBase sovereign data layer (SQLite,
  integer minor units, append-only audit ledger)
- NexusShop: zero-commission marketplace on WhatsApp

## Quickstart

Zero external dependencies - pure Python stdlib:

    python nexuslang.py -i            # interactive
    python nexuslang.py programa.nx   # run a program
    python nexuslang.py --test        # test suite

Or:

    pip install nexuslang
    nexus -i

## Examples

    función saludar(nombre):
        mostrar("Hola " + nombre)
    saludar("Mundo")

    فعل سلام(نام):
        دکھاؤ("سلام " + نام)
    سلام("پاکستان")

## In this repo

- nexuslang.py - language + VM + shop engine
- nexusbase.py - sovereign data layer
- nexusshop/ - marketplace programs (.nx)
- examples/ - sample programs
- TERMS.md - pilot Terms & Privacy
- PAKISTAN_ONEPAGER.md - institutional overview

## License

MIT
EOF
git add -A && git commit -m "README v9.4: trilingue + VM + NexusBase + NexusShop" && git push && echo "PUSHEADO"
