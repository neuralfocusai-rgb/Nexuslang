# NexusLang v9.4

**The first trilingual programming language (Spanish / English / Urdu) with native Urdu script (RTL), its own compiler pipeline and its own virtual machine.**

*El primer lenguaje trilingüe (Español / Inglés / Urdu) con escritura urdu nativa (RTL), compilador propio y máquina virtual propia.*

> **230 million people in Pakistan think in Urdu. Yet almost every programming path on Earth tells them: "Learn English first. Then code."**
> 
> **That's not a technical barrier. It's a closed door.**
> 
> NexusLang is the bridge. Not to replace English — to build the ramp TO it. Because the bridge is not the destination.

**Simple enough for a 10-year-old. Powerful enough for professionals.**

---

##  Hello World in 3 Languages

Same logic. Same VM. Three languages. One bridge.

| Spanish | English | Urdu |
|---------|---------|------|
| `imprimir("Hola, mundo")` | `print("Hello, world")` | `پرنٹ("سلام دنیا")` |

```nexus
# Spanish
función saludar(nombre):
    mostrar("Hola " + nombre)
saludar("Mundo")

# English  
function greet(name):
    show("Hello " + name)
greet("World")

# Urdu
فنکشن سلام(نام):
    دکھاؤ("سلام " + نام)
سلام("دنیا")
```

---

## ✨ What's new since v5

- **v6:** native Urdu keywords + RTL script
- **v8:** compiler pipeline (lexer, parser, AST), bytecode (.nxb) and NexusVM
- **v9:** NexusBase sovereign data layer (SQLite, integer minor units, append-only audit ledger)
- **NexusShop:** zero-commission marketplace on WhatsApp

---

## 🚀 Quickstart

Zero external dependencies - pure Python stdlib:

```bash
python nexuslang.py -i          # interactive
python nexuslang.py programa.nx # run a program
python nexuslang.py --test      # test suite
```

Or:

```bash
pip install nexuslang
nexus -i
```

---

## 📂 In this repo

- `nexuslang.py` - language + VM + shop engine
- `nexusbase.py` - sovereign data layer
- `nexusshop/` - marketplace programs (.nx)
- `examples/` - sample programs
- `TERMS.md` - pilot Terms & Privacy
- `PAKISTAN_ONEPAGER.md` - institutional overview

---

## 🤝 Contributing

NexusLang is built by a global community of educators, developers and native-language advocates.

**We're looking for:**
- 🇵🇰 Urdu native speakers to validate keywords and onboarding
- 🇷 Spanish speakers to expand Latin America adoption
- 🇳🇬 Nigeria partners for West Africa rollout
-  Security advisors for merchant protection
-  Educators piloting in universities

**How to contribute:**
1. Fork the repo
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📊 Current Status

| Component | Status | Version |
|-----------|--------|---------|
| NexusLang Core | ✅ Stable | v9.4 |
| NexusVM | ✅ Stable | v8 |
| NexusBase (Ledger) | ✅ Stable | v9 |
| NexusShop | 🚧 Pilot | v1 |
| Urdu RTL Support | ✅ Stable | v6 |

---

## 🌍 Roadmap

- [ ] NexusShop pilot launch (Pakistan, Nigeria)
- [ ] University pilot program (Virtual University of Pakistan)
- [ ] Mobile app for merchant onboarding
- [ ] Community-contributed keyword libraries (Hindi, Arabic, Portuguese)
- [ ] NexusLang Pro (advanced features for professionals)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 💬 Contact

**Founder:** Lucas Guzmán (Argentina)  
**GitHub:** [neuralfocusai-rgb](https://github.com/neuralfocusai-rgb)  
**LinkedIn:** [Lucas Guzmán](https://linkedin.com/in/lucasguzman)

**Questions?** Open an issue or reach out directly. We respond within 24 hours.

---

<p align="center">
  <strong>Built with ❤️ in Argentina 🇦🇷 · Tested in Pakistan 🇵🇰 · Expanding to Nigeria 🇳🇬</strong>
</p>

## 🏗️ Architecture (v11)

NexusLang v11 is a self-contained language. It does NOT 
translate to Python. Source code runs on its own engine:

1. **Lexer** — tokenizes source (Urdu/Spanish/English 
   keywords), respecting strings and comments.
2. **Parser** — recursive descent, builds an AST.
3. **Interpreter** — tree-walk execution over the AST 
   with scoped environments.

### Own syntax
- Blocks: `{ }`
- Statements end with `;`
- Comments: `//`
- C-style `for` loops

### Own semantics
- Auto-concatenation: `"age: " + 20` works
- Friendly errors in the learner's language
- Trilingual keywords (Urdu / Spanish / English)

> Legacy note: v10.1 (keyword transpiler to Python) is 
> kept for backward compatibility. v11 is the future.

## ✨ Full feature set (v11)

- Imperative: variables, operators, conditionals, loops
  (while, for, break, continue)
- Functions: recursion, closures
- Data: lists [..] with indexing a[0], dicts, strings, math
- OOP: classes (کلاس), self (خود), constructor (نیا),
  methods, attributes
- Modules: درآمد("file.nx")
- File I/O: read / write
- Errors: try/catch (کوشش/پکڑو) + friendly messages
- REPL: interactive shell
- Trilingual: Urdu / Spanish / English
