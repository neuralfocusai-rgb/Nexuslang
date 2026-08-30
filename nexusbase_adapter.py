#!/usr/bin/env python3
# NexusBase Adapter v9.2 — misma API que DB/DBPath de nexuslang.py,
# pero persistido en SQLite (atomico, crash-safe, respaldable)
import json, os
import nexusbase as NB

_JSON_FILE = os.environ.get('NEXUS_DB', 'nexus_db.json')

def _kv_table(con):
    con.execute("CREATE TABLE IF NOT EXISTS kv(id TEXT PRIMARY KEY, data TEXT NOT NULL, updated_at TEXT NOT NULL DEFAULT (datetime('now')))")

def _kv_load():
    con = NB.connect(); _kv_table(con)
    row = con.execute("SELECT data FROM kv WHERE id='root'").fetchone()
    con.close()
    if row:
        try: return json.loads(row[0])
        except Exception: return {}
    if os.path.exists(_JSON_FILE):
        try: return json.load(open(_JSON_FILE, encoding='utf-8'))
        except Exception: return {}
    return {}

def _kv_flush(data):
    con = NB.connect(); _kv_table(con)
    con.execute("INSERT OR REPLACE INTO kv(id,data,updated_at) VALUES ('root',?,datetime('now'))",
                (json.dumps(data, ensure_ascii=False),))
    con.commit(); con.close()

class DB:
    def __init__(self): object.__setattr__(self, '_data', _kv_load())
    def __getattr__(self, name): return DBPath(self._data, [name])
    def guardar(self):
        _kv_flush(self._data)
        return 'DB saved (NexusBase)'

class DBPath:
    def __init__(self, data, path):
        if not path:
            data = _kv_load() or data
        object.__setattr__(self, '_data', data)
        object.__setattr__(self, '_path', path)
    def __getattr__(self, name):
        if name.startswith('_'): raise AttributeError(name)
        return DBPath(self._data, self._path + [name])
    def __setattr__(self, name, value):
        if name.startswith('_'): object.__setattr__(self, name, value)
        else: self.__set(self._path + [name], value)
    def __getitem__(self, key): return DBPath(self._data, self._path + [key])
    def __setitem__(self, key, value): self.__set(self._path + [key], value)
    def __set(self, path, value):
        actual = self._data
        for i, parte in enumerate(path):
            if i == len(path) - 1: actual[parte] = value
            else:
                if not isinstance(actual.get(parte), dict): actual[parte] = {}
                actual = actual[parte]
        _kv_flush(self._data)
    def __read(self):
        actual = self._data
        for parte in self._path:
            if isinstance(actual, dict) and parte in actual: actual = actual[parte]
            else: return None
        return actual
    def get(self): return self.__read()
    def __eq__(self, other): return self.__read() == other
    def __str__(self): return str(self.__read())
    def __repr__(self): return repr(self.__read())
