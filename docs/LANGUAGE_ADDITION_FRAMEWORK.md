# LANGUAGE ADDITION FRAMEWORK (LAF) — NexusLang

Purpose: make adding a native language a repeatable, testable pipeline — not a rewrite.
A language pack is data + tests + docs. The engine stays language-agnostic.

## PIPELINE (8 steps per language)
1. KEYWORD TABLE: langs/<lang>/keywords.json — single-token mappings, NFC-normalized, unique values, no collision with EN reserved words.
2. LEXER RULES: Unicode identifier support (already proven by Urdu RTL); declare script (LTR/RTL) and any bidi handling needed.
3. SYNTAX PATTERNS: loop/conditional pairings (e.g. TR: "her ... için", "eğer ... ise") documented in langs/<lang>/README.
4. TESTS: >=10 green tests in tests/test_<lang>_suite.py running standalone (no engine import) validating table integrity + example coverage.
5. DOCS: quickstart + keyword reference in langs/<lang>/README.md.
6. PLAYGROUND: one runnable example in langs/<lang>/examples/ shown in the browser playground.
7. ERROR MESSAGES: localized message strings for the top 10 runtime/parse errors.
8. RELEASE: version bump + codename (TR = v5.5 "Anadolu") + changelog entry + press angle.

## ACCEPTANCE CRITERIA (merge gate)
- 10/10 tests green on the language branch.
- Example program covers: function, loop, conditional, string concat.
- No main-branch regression (pack is additive-only).

## MAINTENANCE
Every language pack owns its tests forever. Removing a keyword is a breaking change requiring major version bump.
