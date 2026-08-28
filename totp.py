import base64, hmac, hashlib, struct, time
secret = input('Pega la clave secreta de PyPI: ').strip()
key = base64.b32decode(secret)
t = int(time.time()) // 30
h = hmac.new(key, struct.pack('>Q', t), hashlib.sha1).digest()
o = h[19] & 15
code = (struct.unpack('>I', h[o:o+4])[0] & 0x7fffffff) % 1000000
print('TU CODIGO:', f'{code:06d}')
