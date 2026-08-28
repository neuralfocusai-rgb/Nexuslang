src = open('nexusshop/v20.nx').read()
q = chr(34)
n10 = chr(10)
old1 = "color:#fff'>" + n10 + "    html = html + " + q + "<input name='foto'"
new1 = "color:#fff'>" + q + n10 + "    html = html + " + q + "<input name='foto'"
print('fix1 ->', src.count(old1))
src = src.replace(old1, new1, 1)
old2 = "color:#fff'>" + q + q
new2 = "color:#fff'>" + q
print('fix2 ->', src.count(old2))
src = src.replace(old2, new2, 1)
open('nexusshop/v20.nx','w').write(src)
print('FIX v2.3 OK')
