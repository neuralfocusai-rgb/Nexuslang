src = open('nexuslang.py').read()
old_ext = '''_h = "<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'></head><body><h1>\U0001F6D2 " + _nom + "</h1>"
                                for _p in (_st.get('productos') or []):
                                    _h += "<div><b>" + str(_p.get('nombre','')) + "</b> - $" + str(_p.get('precio','')) + "</div>"
                                _h += "<p><a href='https://wa.me/" + str(_st.get('whatsapp','')).replace('+','') + "?text=Quiero%20comprar%20en%20" + _nom + "'>\U0001F4F1 Pedir por WhatsApp</a></p></body></html>"'''
new_basic = '_h = "<html><head><meta charset=\'utf-8\'></head><body><h1>\U0001F6D2 " + _nom + "</h1><p>\u2705 Persistencia NexusBase VIVA.</p></body></html>"'
print('revert ->', src.count(old_ext))
src = src.replace(old_ext, new_basic)
open('nexuslang.py','w').write(src)
print('OK')
