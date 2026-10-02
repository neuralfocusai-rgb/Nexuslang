import json, os, re, sys, unicodedata as ud
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KW = os.path.join(ROOT, "langs", "turkish", "keywords.json")
EX = os.path.join(ROOT, "langs", "turkish", "examples", "merhaba.nx")
DOC = os.path.join(ROOT, "docs", "LANGUAGE_ADDITION_FRAMEWORK.md")
EN_RESERVED = {"if","else","for","while","function","return","and","or","not","true","false","null","class","import","try","catch","break","continue","print","in","range","len","input","then"}
passed = failed = 0
def check(name, cond):
    global passed, failed
    if cond: passed += 1; print("PASS", name)
    else: failed += 1; print("FAIL", name)
data = json.load(open(KW, encoding="utf-8"))["tr"]
check("01 keywords load & >=20", isinstance(data, dict) and len(data) >= 20)
check("02 values non-empty", all(isinstance(v, str) and v.strip() for v in data.values()))
check("03 values unique", len(set(data.values())) == len(data))
check("04 turkish chars present", any(ch in "".join(data.values()) for ch in "ğüöçşıĞÜÖÇŞİ"))
check("05 NFC normalized", all(k == ud.normalize("NFC", k) and v == ud.normalize("NFC", v) for k, v in data.items()))
check("06 no EN reserved as TR keyword", not (set(data.values()) & EN_RESERVED))
src = open(EX, encoding="utf-8").read()
check("07 example exists & non-empty", len(src) > 50)
kwv = set(data.values())
check("08 core TR keywords in table", {"yaz","fonksiyon","eğer","yoksa","her","için","aralık"} <= kwv)
check("09 example has fn+loop+cond", ("fonksiyon" in src) and ("her" in src) and ("eğer" in src))
doc = open(DOC, encoding="utf-8").read()
check("10 framework doc sections", all(s in doc for s in ["KEYWORD TABLE","LEXER","TESTS","PLAYGROUND","RELEASE"]))
print(f"\n{passed}/10 PASS, {failed} FAIL")
sys.exit(1 if failed else 0)
