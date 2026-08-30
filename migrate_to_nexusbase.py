#!/usr/bin/env python3
import json, os
import nexusbase as NB

con = NB.connect(); NB.init(con)

src = {}
if os.path.exists('nexus_db.json'):
    try:
        src = json.load(open('nexus_db.json', encoding='utf-8'))
    except Exception as e:
        print('JSON ERROR:', e)
print('KEYS JSON:', list(src.keys()) if isinstance(src, dict) else type(src))

def rows_of(key):
    v = src.get(key, []) if isinstance(src, dict) else []
    if isinstance(v, dict): v = list(v.values())
    return v if isinstance(v, list) else []

def guess_id(rec, i, tag):
    if isinstance(rec, dict):
        for k in ('id', '_id', 'uuid', 'merchant_id', 'store_id'):
            if rec.get(k): return str(rec[k])
        for k in ('name', 'whatsapp', 'phone'):
            if rec.get(k): return '%s:%s:%d' % (tag, rec[k], i)
    return '%s:auto:%d' % (tag, i)

def get(rec, *keys, dflt=None):
    if isinstance(rec, dict):
        for k in keys:
            if rec.get(k) is not None: return rec[k]
    return dflt

def norm(v, allowed, dflt):
    return v if v in allowed else dflt

def ensure_merchant(mid):
    con.execute('INSERT OR IGNORE INTO merchants(id,name,whatsapp,status,data) VALUES (?,?,?,?,?)',
                (mid, mid, '', 'active', '{}'))

counts = {}
for tag, table in (('merchant', 'merchants'), ('product', 'products'), ('order', 'orders')):
    rows = rows_of(table)
    for i, rec in enumerate(rows):
        rid = guess_id(rec, i, tag)
        data = json.dumps(rec, ensure_ascii=False) if isinstance(rec, (dict, list)) else json.dumps({'value': rec}, ensure_ascii=False)
        if table == 'merchants':
            con.execute('INSERT OR IGNORE INTO merchants(id,name,whatsapp,status,data) VALUES (?,?,?,?,?)',
                (rid, str(get(rec, 'name', 'store', 'shop', dflt=rid)),
                 str(get(rec, 'whatsapp', 'phone', dflt='')),
                 norm(get(rec, 'status', dflt='active'), ('active', 'suspended', 'closed'), 'active'), data))
        else:
            mid = str(get(rec, 'merchant_id', 'owner', 'store_id', dflt='unknown'))
            ensure_merchant(mid)
            if table == 'products':
                con.execute('INSERT OR IGNORE INTO products(id,merchant_id,name,price_minor,currency,status,data) VALUES (?,?,?,?,?,?,?)',
                    (rid, mid, str(get(rec, 'name', 'title', dflt=rid)),
                     NB.to_minor(get(rec, 'price', dflt=0)),
                     str(get(rec, 'currency', dflt='PKR')),
                     norm(get(rec, 'status', dflt='live'), ('live', 'paused', 'deleted'), 'live'), data))
            else:
                con.execute('INSERT OR IGNORE INTO orders(id,merchant_id,total_minor,currency,status,data) VALUES (?,?,?,?,?,?)',
                    (rid, mid, NB.to_minor(get(rec, 'total', 'amount', dflt=0)),
                     str(get(rec, 'currency', dflt='PKR')),
                     norm(get(rec, 'status', dflt='created'), ('created', 'paid', 'fulfilled', 'refunded', 'cancelled'), 'created'), data))
    counts[table] = len(rows)
con.commit()

NB.append_ledger(con, 'system', 'migration', 'json_to_nexusbase', 0, 'PKR', json.dumps(counts))
con.commit()
print('MIGRADO:', counts)
for t in ('merchants', 'products', 'orders', 'ledger'):
    print(t, '=', con.execute('SELECT COUNT(*) FROM %s' % t).fetchone()[0])
print('SCHEMA OK')
