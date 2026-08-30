#!/usr/bin/env python3
# NexusBase v9.0 — sovereign data layer
# SQLite serverless + integer minor units + append-only ledger
import sqlite3, json, os

DB = 'nexusbase.db'

SCHEMA = '''
CREATE TABLE IF NOT EXISTS merchants(
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  whatsapp TEXT,
  status TEXT NOT NULL DEFAULT 'active'
    CHECK(status IN ('active','suspended','closed')),
  data TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS products(
  id TEXT PRIMARY KEY,
  merchant_id TEXT NOT NULL REFERENCES merchants(id),
  name TEXT NOT NULL,
  price_minor INTEGER NOT NULL CHECK(price_minor >= 0),
  currency TEXT NOT NULL DEFAULT 'PKR',
  status TEXT NOT NULL DEFAULT 'live'
    CHECK(status IN ('live','paused','deleted')),
  data TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS orders(
  id TEXT PRIMARY KEY,
  merchant_id TEXT NOT NULL REFERENCES merchants(id),
  total_minor INTEGER NOT NULL CHECK(total_minor >= 0),
  currency TEXT NOT NULL DEFAULT 'PKR',
  status TEXT NOT NULL DEFAULT 'created'
    CHECK(status IN ('created','paid','fulfilled','refunded','cancelled')),
  data TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS ledger(
  seq INTEGER PRIMARY KEY AUTOINCREMENT,
  entity_type TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  amount_minor INTEGER NOT NULL DEFAULT 0,
  currency TEXT NOT NULL DEFAULT 'PKR',
  note TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_orders_merchant ON orders(merchant_id);
CREATE INDEX IF NOT EXISTS idx_products_merchant ON products(merchant_id);
CREATE INDEX IF NOT EXISTS idx_ledger_entity ON ledger(entity_type, entity_id);
'''

def connect(db=DB):
    con = sqlite3.connect(db)
    con.execute('PRAGMA foreign_keys = ON')
    return con

def init(con):
    con.executescript(SCHEMA)
    con.commit()

def to_minor(x):
    try:
        return int(round(float(x) * 100))
    except Exception:
        return 0

def append_ledger(con, etype, eid, event, amount_minor=0, currency='PKR', note=None):
    con.execute(
        'INSERT INTO ledger(entity_type,entity_id,event_type,amount_minor,currency,note) VALUES (?,?,?,?,?,?)',
        (etype, eid, event, amount_minor, currency, note))

def backup(src_db=DB, dst='nexusbase.backup.db'):
    a = sqlite3.connect(src_db); b = sqlite3.connect(dst)
    a.backup(b); a.close(); b.close()
    return dst
