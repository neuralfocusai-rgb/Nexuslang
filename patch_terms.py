import sys
src = open('nexuslang.py', encoding='utf-8').read()
if 'TERMS-WIRED' in src:
    print('TERMS YA CABLEADO'); sys.exit(0)
lines = src.split('\n')
i = next(k for k, l in enumerate(lines)
         if l.strip().startswith('def do_GET'))
j = next(k for k in range(i, i + 6)
         if lines[k].strip() == 's = self')
css = "font-family:monospace;max-width:860px;"
css += "margin:30px auto;line-height:1.55;padding:0 16px"
html1 = "<html><head><meta charset='utf-8'>"
html1 += "<title>NexusShop Terms</title></head>"
html1 += "<body style='" + css + "'>"
html1 += "<pre style='white-space:pre-wrap'>"
html2 = "</pre><p><a href='/'>NexusShop</a></p>"
html2 += "</body></html>"
block = []
block.append("        if s.path.startswith('/terms'):  # TERMS-WIRED")
block.append("            try:")
block.append("                _t = open('TERMS.md', encoding='utf-8').read()")
block.append("            except Exception:")
block.append("                _t = 'Terms unavailable.'")
block.append("            _h = " + repr(html1) +
             " + _t.replace('<', '&lt;') + " + repr(html2))
block.append("            s.send_response(200)")
block.append("            s.send_header('Content-Type', 'text/html; charset=utf-8')")
block.append("            s.end_headers()")
block.append("            s.wfile.write(_h.encode('utf-8'))")
block.append("            return")
lines[j + 1:j + 1] = block
open('nexuslang.py', 'w', encoding='utf-8').write('\n'.join(lines))
print('RUTA /terms CABLEADA')
nx = open('nexusshop/v12.nx', encoding='utf-8').read()
old = "Ayuda</a></div>"
add = "<a href='/terms' style='color:lightgrey;"
add += "text-decoration:none;font-size:14px'>"
add += "Términos</a></div>"
if old in nx and 'Términos</a>' not in nx:
    nx = nx.replace(old, add)
    open('nexusshop/v12.nx', 'w', encoding='utf-8').write(nx)
    print('FOOTER ACTUALIZADO')
else:
    print('FOOTER SIN CAMBIOS')
