#!/usr/bin/env python3
import json
import nexusbase as NB

con = NB.connect(); NB.init(con)
con.execute("CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY, name TEXT, data TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT (datetime('now')))")

src = json.load(open('nexus_db.json', encoding='utf-8'))
tiendas = src.get('nexusshop', {}).get('tiendas', {})

m = p = 0
for slug, t in tiendas.items():
    if not isinstance(t, dict): continue
    con.execute('INSERT OR REPLACE INTO merchants(id,name,whatsapp,status,data) VALUES (?,?,?,?,?)',
        (slug, str(t.get('nombre', slug)), str(t.get('whatsapp', '')), 'active',
         json.dumps(t, ensure_ascii=False)))
    m += 1
    for i, pr in enumerate(t.get('productos', []) or []):
        pid = '%s:p%d' % (slug, i)
        con.execute('INSERT OR REPLACE INTO products(id,merchant_id,name,price_minor,currency,status,data) VALUES (?,?,?,?,?,?,?)',
            (pid, slug, str(pr.get('nombre', pid)), NB.to_minor(pr.get('precio', 0)), 'USD', 'live',
             json.dumps(pr, ensure_ascii=False)))
        p += 1

for uid, u in src.get('usuarios', {}).items():
    name = u.get('nombre', uid) if isinstance(u, dict) else str(u)
    con.execute('INSERT OR REPLACE INTO users(id,name,data) VALUES (?,?,?)',
        (uid, str(name), json.dumps(u, ensure_ascii=False)))
con.commit()

NB.append_ledger(con, 'system', 'migration', 'v91_tiendas_to_nexusbase', 0, 'USD',
                 json.dumps({'merchants': m, 'products': p}))
con.commit()
print('MIGRADO v9.1: merchants =', m, '| products =', p)
for t in ('merchants', 'products', 'orders', 'ledger', 'users'):
    print(t, '=', con.execute('SELECT COUNT(*) FROM %s' % t).fetchone()[0])
print('SAMPLE PRODUCTS:', con.execute('SELECT id, price_minor, currency FROM products LIMIT 3').fetchall())
NB.backup()
print('BACKUP OK')
