#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import nexuslang_v12 as nx

TESTS = [
    ("variables",   'متغیر x = 5;\nلکھو(x);', "5"),
    ("concat",      'متغیر n = "علی";\nلکھو("سلام " + n);', "سلام علی"),
    ("math",        'لکھو(7 % 3);', "1"),
    ("if_else",     'متغیر x = 10;\nاگر (x > 5) { لکھو("بڑا"); } ورنہ { لکھو("چھوٹا"); }', "بڑا"),
    ("while",       'متغیر i = 1;\nجبکہ (i <= 3) { لکھو(i); i = i + 1; }', "1\n2\n3"),
    ("for",         'برائے (متغیر i = 0; i < 3; i = i + 1) { لکھو(i); }', "0\n1\n2"),
    ("funcion",     'طریقہ جمع(a, b) { واپس a + b; }\nلکھو(جمع(2, 3));', "5"),
    ("clase",       'کلاس ط { طریقہ init(n) { خود.n = n; } طریقہ دکھاؤ() { لکھو(خود.n); } }\nمتغیر o = نیا ط("سلام");\no.دکھاؤ();', "سلام"),
    ("array",       'متغیر a = [1, 2, 3];\nلکھو(a[1]);', "2"),
    ("try_catch",   'کوشش { متغیر x = 1 / 0; } پکڑو (e) { لکھو("پکڑا"); }', "پکڑا"),
    ("break",       'متغیر i = 0;\nجبکہ (صحيح) { i = i + 1; اگر (i == 2) { توڑو; } لکھو(i); }', "1"),
    ("urdu_comma",  'کلاس ط { طریقہ init(a، b) { خود.a = a; } }\nمتغیر o = نیا ط(1، 2);\nلکھو(o.a);', "1"),
    ("elif",        'متغیر x = 7;\nاگر (x > 10) { لکھو("زیادہ"); } ورنہ اگر (x > 5) { لکھو("درمیانہ"); } ورنہ { لکھو("کم"); }', "درمیانہ"),
    ("plus_eq",     'متغیر i = 1;\ni += 4;\nلکھو(i);', "5"),
    ("plusplus",    'متغیر i = 1;\ni++;\nلکھو(i);', "2"),
    ("length",      'متغیر a = [1, 2, 3];\nلکھو(a.length);', "3"),
    ("push",        'متغیر a = [1];\na.push(2);\nلکھو(a.length);', "2"),
    ("urdu_digits", 'متغیر x = ۲۵;\nلکھو(x);', "25"),
]

fails = 0
for name, code, exp in TESTS:
    got = nx.run_code(code).strip()
    if got == exp:
        print(f"✅ {name}")
    else:
        fails += 1
        print(f"❌ {name}: esperado {exp!r} pero dio {got!r}")

if fails == 0:
    print("🎉 TODOS LOS TESTS PASARON")
else:
    print(f"⛔ {fails} TESTS FALLARON")
sys.exit(1 if fails else 0)
