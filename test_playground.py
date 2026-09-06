tests = [
    ("Variables básicas", '''
متغیر نام = "حماد";
لکھو("سلام " + نام);
'''),
    ("Aritmética", '''
متغیر x = 10;
متغیر y = 3;
لکھو(x + y);
لکھو(x - y);
'''),
    ("Módulo", '''
متغیر n = 10;
لکھو(n % 3);
'''),
    ("Funciones", '''
طریقہ دوبلہ(num) {
    واپس num * 2;
}
لکھو(doubl(5));
'''),
]

print("Tests listos. Copiá y pegá cada uno en el playground.")
for name, code in tests:
    print(f"\n=== {name} ===")
    print(code)
