lines = open('nexusshop/v19.nx').readlines()
lines[120] = "        contenido = contenido + \"<div style='text-align:center;margin:8px 0 16px'><b style='color:white;font-size:34px;text-shadow:0 0 14px aqua'>Nexus<span style='color:aqua'>Shop</span></b></div>\"\n"
open('nexusshop/v19.nx','w').writelines(lines)
print('OK', lines[120].count('"'))
