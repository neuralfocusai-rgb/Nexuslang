import os, json, re, base64, hashlib, secrets, shutil
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ==================== CONFIGURACIÓN ====================
VERSION = "5.1.0"
PUERTO = 8080
DIRECTORIO_DATOS = "nexus_data"
DIRECTORIO_REPO = "nexus_repo"
DIRECTORIO_FILES = "nexus_files"
DIRECTORIO_BACKUPS = "nexus_backups"
DIRECTORIO_LOGS = "nexus_logs"
ARCHIVO_USUARIOS = "nexus_users.json"
ARCHIVO_API_KEYS = "nexus_api_keys.json"

for dir in [DIRECTORIO_DATOS, DIRECTORIO_REPO, DIRECTORIO_FILES, DIRECTORIO_BACKUPS, DIRECTORIO_LOGS]:
    if not os.path.exists(dir): os.makedirs(dir)

# ==================== ENCRYPTACIÓN AES-256-GCM REAL ====================
MASTER_KEY = hashlib.sha256("nexus_sovereign_2026_argentina_china".encode()).digest()
NONCE_SIZE = 12

def encrypt_data(plaintext):
    """Encripta con AES-256-GCM (nivel militar)"""
    nonce = os.urandom(NONCE_SIZE)
    aesgcm = AESGCM(MASTER_KEY)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
    return base64.b64encode(nonce + ciphertext).decode('utf-8')

def decrypt_data(encrypted_data):
    """Desencripta datos AES-256-GCM"""
    encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
    nonce = encrypted_bytes[:NONCE_SIZE]
    ciphertext = encrypted_bytes[NONCE_SIZE:]
    aesgcm = AESGCM(MASTER_KEY)
    return aesgcm.decrypt(nonce, ciphertext, None).decode('utf-8')

# ==================== GESTIÓN DE USUARIOS ====================
def hash_password(password, salt=None):
    if salt is None: salt = secrets.token_hex(32)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return hashed.hex(), salt

def crear_usuario(username, password, email=None, role="user"):
    if not os.path.exists(ARCHIVO_USUARIOS): usuarios = {}
    else:
        with open(ARCHIVO_USUARIOS, "r") as f: usuarios = json.load(f)
    if username in usuarios: return False
    hashed, salt = hash_password(password)
    usuarios[username] = {
        "password": hashed, "salt": salt,
        "email": email or f"{username}@nexus.local",
        "role": role, "created": datetime.now().isoformat(),
        "last_login": None, "active": True
    }
    with open(ARCHIVO_USUARIOS, "w") as f: json.dump(usuarios, f, indent=2)
    log_event("USER_CREATED", username, f"Role: {role}")
    return True

def verificar_usuario(username, password):
    if not os.path.exists(ARCHIVO_USUARIOS): return False, None
    with open(ARCHIVO_USUARIOS, "r") as f: usuarios = json.load(f)
    if username not in usuarios: return False, None
    user = usuarios[username]
    if not user["active"]: return False, None
    hashed, _ = hash_password(password, user["salt"])
    if hashed == user["password"]:
        user["last_login"] = datetime.now().isoformat()
        with open(ARCHIVO_USUARIOS, "w") as f: json.dump(usuarios, f, indent=2)
        return True, user
    return False, None

def generar_api_key(username):
    if not os.path.exists(ARCHIVO_API_KEYS): keys = {}
    else:
        with open(ARCHIVO_API_KEYS, "r") as f: keys = json.load(f)
    api_key = f"nexus_{username}_{secrets.token_hex(24)}"
    keys[api_key] = {
        "user": username, "created": datetime.now().isoformat(),
        "active": True, "requests": 0, "last_used": None, "rate_limit": 1000
    }
    with open(ARCHIVO_API_KEYS, "w") as f: json.dump(keys, f, indent=2)
    log_event("API_KEY_CREATED", username, f"Key: {api_key[:20]}...")
    return api_key

def log_event(event_type, user, details=""):
    log_file = os.path.join(DIRECTORIO_LOGS, f"{datetime.now().strftime('%Y%m')}.json")
    if not os.path.exists(log_file): logs = []
    else:
        with open(log_file, "r") as f: logs = json.load(f)
    logs.append({
        "timestamp": datetime.now().isoformat(),
        "event": event_type, "user": user, "details": details, "ip": "localhost"
    })
    with open(log_file, "w") as f: json.dump(logs, f, indent=2)

# ==================== NEXUSLANG AVANZADO ====================
def interpretar_nexus_lang(comando, user_session=None):
    comando = comando.strip()
    try:
        if comando.startswith("GUARDAR"):
            c = re.match(r"^GUARDAR\s+USUARIO:([\w\d_]+)\s+DATO:([\w\d_]+)\s+VALOR:\"(.+?)\"$", comando)
            if not c: return {"estado": "error", "mensaje": "Syntax: GUARDAR USUARIO:id DATO:key VALOR:\"value\""}
            usuario, dato, valor = c.groups()
            if user_session and usuario != user_session: return {"estado": "error", "mensaje": "Unauthorized"}
            carpeta = os.path.join(DIRECTORIO_DATOS, usuario)
            if not os.path.exists(carpeta): os.makedirs(carpeta)
            archivo = os.path.join(carpeta, "datos.json")
            datos = {}
            if os.path.exists(archivo):
                with open(archivo, "r", encoding="utf-8") as f: datos = json.load(f)
            datos[dato] = encrypt_data(valor)  # AES-256-GCM REAL
            with open(archivo, "w", encoding="utf-8") as f: json.dump(datos, f, indent=4, ensure_ascii=False)
            log_event("GUARDAR", usuario, f"Dato: {dato}")
            return {"estado": "exito", "mensaje": f"Data '{dato}' saved for {usuario}"}
        
        elif comando.startswith("LEER"):
            c = re.match(r"^LEER\s+USUARIO:([\w\d_]+)\s+DATO:([\w\d_]+)$", comando)
            if not c: return {"estado": "error", "mensaje": "Syntax: LEER USUARIO:id DATO:key"}
            usuario, dato = c.groups()
            if user_session and usuario != user_session: return {"estado": "error", "mensaje": "Unauthorized"}
            archivo = os.path.join(DIRECTORIO_DATOS, usuario, "datos.json")
            if not os.path.exists(archivo): return {"estado": "error", "mensaje": f"User '{usuario}' not found"}
            with open(archivo, "r", encoding="utf-8") as f: datos = json.load(f)
            if dato in datos:
                valor = decrypt_data(datos[dato])  # AES-256-GCM REAL
                return {"estado": "exito", "mensaje": f"Value of '{dato}': {valor}"}
            return {"estado": "error", "mensaje": f"Key '{dato}' not found"}
        
        elif comando.startswith("UPDATE"):
            c = re.match(r"^UPDATE\s+USUARIO:([\w\d_]+)\s+DATO:([\w\d_]+)\s+VALOR:\"(.+?)\"$", comando)
            if not c: return {"estado": "error", "mensaje": "Syntax: UPDATE USUARIO:id DATO:key VALOR:\"value\""}
            usuario, dato, valor = c.groups()
            if user_session and usuario != user_session: return {"estado": "error", "mensaje": "Unauthorized"}
            archivo = os.path.join(DIRECTORIO_DATOS, usuario, "datos.json")
            if not os.path.exists(archivo): return {"estado": "error", "mensaje": f"User '{usuario}' not found"}
            with open(archivo, "r", encoding="utf-8") as f: datos = json.load(f)
            if dato not in datos: return {"estado": "error", "mensaje": f"Key '{dato}' not found"}
            datos[dato] = encrypt_data(valor)
            with open(archivo, "w", encoding="utf-8") as f: json.dump(datos, f, indent=4, ensure_ascii=False)
            log_event("UPDATE", usuario, f"Dato: {dato}")
            return {"estado": "exito", "mensaje": f"Data '{dato}' updated"}
        
        elif comando.startswith("DELETE"):
            c = re.match(r"^DELETE\s+USUARIO:([\w\d_]+)\s+DATO:([\w\d_]+)$", comando)
            if not c: return {"estado": "error", "mensaje": "Syntax: DELETE USUARIO:id DATO:key"}
            usuario, dato = c.groups()
            if user_session and usuario != user_session: return {"estado": "error", "mensaje": "Unauthorized"}
            archivo = os.path.join(DIRECTORIO_DATOS, usuario, "datos.json")
            if not os.path.exists(archivo): return {"estado": "error", "mensaje": f"User '{usuario}' not found"}
            with open(archivo, "r", encoding="utf-8") as f: datos = json.load(f)
            if dato not in datos: return {"estado": "error", "mensaje": f"Key '{dato}' not found"}
            del datos[dato]
            with open(archivo, "w", encoding="utf-8") as f: json.dump(datos, f, indent=4, ensure_ascii=False)
            log_event("DELETE", usuario, f"Dato: {dato}")
            return {"estado": "exito", "mensaje": f"Data '{dato}' deleted"}
        
        elif comando.startswith("LIST"):
            c = re.match(r"^LIST\s+USUARIO:([\w\d_]+)$", comando)
            if not c: return {"estado": "error", "mensaje": "Syntax: LIST USUARIO:id"}
            usuario = c.group(1)
            if user_session and usuario != user_session: return {"estado": "error", "mensaje": "Unauthorized"}
            archivo = os.path.join(DIRECTORIO_DATOS, usuario, "datos.json")
            if not os.path.exists(archivo): return {"estado": "error", "mensaje": f"User '{usuario}' not found"}
            with open(archivo, "r", encoding="utf-8") as f: datos = json.load(f)
            return {"estado": "exito", "mensaje": f"Keys for {usuario}", "data": list(datos.keys()), "count": len(datos)}
        
        elif comando.startswith("SNAPSHOT"):
            c = re.match(r"^SNAPSHOT\s+USUARIO:([\w\d_]+)$", comando)
            if not c: return {"estado": "error", "mensaje": "Syntax: SNAPSHOT USUARIO:id"}
            usuario = c.group(1)
            if user_session and usuario != user_session: return {"estado": "error", "mensaje": "Unauthorized"}
            carpeta_origen = os.path.join(DIRECTORIO_DATOS, usuario)
            if not os.path.exists(carpeta_origen): return {"estado": "error", "mensaje": f"User '{usuario}' not found"}
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            carpeta_destino = os.path.join(DIRECTORIO_BACKUPS, f"{usuario}_{timestamp}")
            shutil.copytree(carpeta_origen, carpeta_destino)
            log_event("SNAPSHOT", usuario, f"Timestamp: {timestamp}")
            return {"estado": "exito", "mensaje": f"Snapshot created: {usuario}_{timestamp}"}
        
        elif comando.startswith("SEARCH"):
            c = re.match(r"^SEARCH\s+QUERY:\"(.+?)\"$", comando)
            if not c: return {"estado": "error", "mensaje": "Syntax: SEARCH QUERY:\"term\""}
            query = c.group(1).lower()
            results = []
            for usuario in os.listdir(DIRECTORIO_DATOS):
                archivo = os.path.join(DIRECTORIO_DATOS, usuario, "datos.json")
                if os.path.exists(archivo):
                    with open(archivo, "r", encoding="utf-8") as f: datos = json.load(f)
                    for key, val in datos.items():
                        try:
                            val_decoded = decrypt_data(val)
                            if query in key.lower() or query in val_decoded.lower():
                                results.append({"user": usuario, "key": key, "value": val_decoded[:50]})
                        except: pass
            return {"estado": "exito", "mensaje": f"Found {len(results)} results", "data": results}
        
        elif comando.startswith("COMMIT"):
            c = re.match(r"^COMMIT\s+USUARIO:([\w\d_]+)\s+MESSAGE:\"(.+?)\"$", comando)
            if not c: return {"estado": "error", "mensaje": "Syntax: COMMIT USUARIO:id MESSAGE:\"msg\""}
            usuario, message = c.groups()
            if user_session and usuario != user_session: return {"estado": "error", "mensaje": "Unauthorized"}
            carpeta_origen = os.path.join(DIRECTORIO_DATOS, usuario)
            if not os.path.exists(carpeta_origen): return {"estado": "error", "mensaje": f"User '{usuario}' not found"}
            repo_dir = os.path.join(DIRECTORIO_REPO, usuario)
            if not os.path.exists(repo_dir): os.makedirs(repo_dir)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            commit_file = os.path.join(repo_dir, f"commit_{timestamp}.json")
            commit_data = {"timestamp": timestamp, "message": message, "files": []}
            if os.path.exists(os.path.join(carpeta_origen, "datos.json")):
                commit_data["files"].append("datos.json")
                shutil.copy(os.path.join(carpeta_origen, "datos.json"), os.path.join(repo_dir, f"datos_{timestamp}.json"))
            with open(commit_file, "w") as f: json.dump(commit_data, f, indent=2)
            log_event("COMMIT", usuario, f"Message: {message}")
            return {"estado": "exito", "mensaje": f"Commit created: {timestamp}"}
        
        elif comando.startswith("LOGS"):
            if user_session:
                log_file = os.path.join(DIRECTORIO_LOGS, f"{datetime.now().strftime('%Y%m')}.json")
                if os.path.exists(log_file):
                    with open(log_file, "r") as f: logs = json.load(f)
                    user_logs = [l for l in logs if l["user"] == user_session]
                    return {"estado": "exito", "mensaje": f"Found {len(user_logs)} logs", "data": user_logs[-10:]}
                return {"estado": "exito", "mensaje": "No logs", "data": []}
            return {"estado": "error", "mensaje": "Unauthorized"}
        
        elif comando.startswith("STATUS"):
            stats = {"users": 0, "total_data": 0, "backups": 0, "api_keys": 0}
            if os.path.exists(ARCHIVO_USUARIOS):
                with open(ARCHIVO_USUARIOS, "r") as f: stats["users"] = len(json.load(f))
            for root, dirs, files in os.walk(DIRECTORIO_DATOS):
                stats["total_data"] += sum(os.path.getsize(os.path.join(root, f)) for f in files)
            stats["backups"] = len(os.listdir(DIRECTORIO_BACKUPS))
            if os.path.exists(ARCHIVO_API_KEYS):
                with open(ARCHIVO_API_KEYS, "r") as f: stats["api_keys"] = len(json.load(f))
            return {"estado": "exito", "mensaje": "System status", "stats": stats}
        
        return {"estado": "error", "mensaje": "Unknown command. Use: GUARDAR, LEER, UPDATE, DELETE, LIST, SNAPSHOT, SEARCH, COMMIT, LOGS, STATUS"}
    except Exception as e:
        return {"estado": "error", "mensaje": str(e)}

# ==================== INTERFAZ WEB ====================
HTML_PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Nexus Platform v{VERSION}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI',Roboto,sans-serif;background:linear-gradient(135deg,#0a0a0a 0%,#1a1a2e 50%,#16213e 100%);min-height:100vh;color:#fff}}
.container{{max-width:1400px;margin:0 auto;padding:20px}}
header{{text-align:center;padding:40px 0;border-bottom:2px solid rgba(0,114,206,0.3);margin-bottom:30px}}
.logo{{font-size:4em;font-weight:300;background:linear-gradient(135deg,#0072CE,#FFD100);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.tagline{{color:#888;font-size:1.2em;letter-spacing:2px}}
.panel{{background:rgba(255,255,255,0.05);backdrop-filter:blur(10px);border-radius:20px;padding:30px;margin:20px 0;border:1px solid rgba(255,255,255,0.1)}}
.input-group{{margin-bottom:20px}}
.input-group input,.input-group textarea{{width:100%;padding:15px;border:1px solid rgba(255,255,255,0.1);border-radius:10px;background:rgba(255,255,255,0.05);color:#fff;font-size:1em;outline:none}}
.btn{{padding:15px 30px;border:none;border-radius:10px;background:linear-gradient(135deg,#0072CE,#005bb5);color:#fff;font-size:1em;font-weight:600;cursor:pointer;margin:5px}}
.btn:hover{{transform:translateY(-2px);box-shadow:0 5px 20px rgba(0,114,206,0.4)}}
.btn-secondary{{background:rgba(255,255,255,0.1)}}
.btn-danger{{background:linear-gradient(135deg,#dc3545,#c82333)}}
.btn-success{{background:linear-gradient(135deg,#28a745,#1e7e34)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px}}
.card{{background:rgba(255,255,255,0.05);border-radius:15px;padding:25px;border:1px solid rgba(255,255,255,0.1)}}
.card h3{{margin-bottom:15px;color:#0072CE}}
.stat{{font-size:2.5em;font-weight:bold;background:linear-gradient(135deg,#0072CE,#FFD100);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.hidden{{display:none}}
.nav-tabs{{display:flex;gap:10px;margin-bottom:30px;flex-wrap:wrap;border-bottom:2px solid rgba(255,255,255,0.1);padding-bottom:10px}}
.nav-tab{{padding:12px 25px;border:1px solid rgba(255,255,255,0.2);border-radius:25px;background:rgba(255,255,255,0.05);color:#fff;cursor:pointer}}
.nav-tab.active{{background:#0072CE;border-color:#0072CE}}
.response{{padding:25px;border-radius:15px;background:rgba(0,0,0,0.5);margin:20px 0;font-family:monospace;white-space:pre-wrap;display:none}}
.response.success{{border-left:4px solid #4ade80;background:rgba(74,222,128,0.1)}}
.response.error{{border-left:4px solid #f87171;background:rgba(248,113,113,0.1)}}
.user-info{{display:flex;justify-content:space-between;align-items:center;margin-bottom:30px;padding:20px;background:rgba(0,114,206,0.1);border-radius:15px}}
footer{{text-align:center;padding:40px;color:#444;border-top:1px solid rgba(255,255,255,0.1);margin-top:50px}}
.security-badge{{display:inline-block;padding:8px 16px;background:rgba(74,222,128,0.2);border:1px solid #4ade80;border-radius:20px;color:#4ade80;font-size:0.85em;margin-top:10px}}
</style>
</head>
<body>
<div class="container">
<header>
<h1 class="logo">Nexus</h1>
<p class="tagline">Sovereign Intelligence Platform v{VERSION}</p>
<div class="security-badge">🔒 AES-256-GCM Encryption | Zero US Cloud</div>
</header>

<div id="authPanel" class="panel">
<h2 style="margin-bottom:30px;text-align:center">Authentication Center</h2>
<div class="grid">
<div class="card">
<h3>Login</h3>
<div class="input-group"><input type="text" id="loginUser" placeholder="Username"></div>
<div class="input-group"><input type="password" id="loginPass" placeholder="Password"></div>
<button class="btn" style="width:100%" onclick="doLogin()">Login</button>
</div>
<div class="card">
<h3>Register</h3>
<div class="input-group"><input type="text" id="regUser" placeholder="Username"></div>
<div class="input-group"><input type="password" id="regPass" placeholder="Password"></div>
<button class="btn btn-secondary" style="width:100%" onclick="doRegister()">Register</button>
</div>
</div>
</div>

<div id="mainPanel" class="panel hidden">
<div class="user-info">
<div>
<span style="color:#888">Welcome: </span><strong id="currentUser" style="color:#0072CE;font-size:1.3em"></strong>
<span id="userRole" style="margin-left:15px;padding:5px 15px;background:rgba(0,114,206,0.3);border-radius:15px;font-size:0.85em"></span>
</div>
<button class="btn btn-danger" onclick="doLogout()">Logout</button>
</div>

<div class="nav-tabs">
<div class="nav-tab active" onclick="showTab('commands')">Commands</div>
<div class="nav-tab" onclick="showTab('repo')">NexusRepo</div>
<div class="nav-tab" onclick="showTab('files')">Files</div>
<div class="nav-tab" onclick="showTab('api')">API Keys</div>
<div class="nav-tab" onclick="showTab('stats')">Statistics</div>
<div class="nav-tab" onclick="showTab('logs')">Audit Logs</div>
</div>

<div id="tab-commands" class="tab-content">
<div class="card">
<h3>NexusLang Command Center</h3>
<div class="input-group">
<textarea id="command" rows="4" placeholder='Available commands:
GUARDAR USUARIO:user DATO:key VALOR:"value"
LEER USUARIO:user DATO:key
UPDATE USUARIO:user DATO:key VALOR:"newvalue"
DELETE USUARIO:user DATO:key
LIST USUARIO:user
SNAPSHOT USUARIO:user
SEARCH QUERY:"term"
COMMIT USUARIO:user MESSAGE:"msg"
LOGS
STATUS'></textarea>
</div>
<div style="margin-bottom:20px">
<button class="btn" onclick="setCmd('GUARDAR USUARIO:user DATO:key VALOR:&quot;value&quot;')">GUARDAR</button>
<button class="btn" onclick="setCmd('LEER USUARIO:user DATO:key')">LEER</button>
<button class="btn" onclick="setCmd('UPDATE USUARIO:user DATO:key VALOR:&quot;newvalue&quot;')">UPDATE</button>
<button class="btn" onclick="setCmd('DELETE USUARIO:user DATO:key')">DELETE</button>
<button class="btn" onclick="setCmd('LIST USUARIO:user')">LIST</button>
<button class="btn" onclick="setCmd('SNAPSHOT USUARIO:user')">SNAPSHOT</button>
<button class="btn" onclick="setCmd('SEARCH QUERY:&quot;term&quot;')">SEARCH</button>
<button class="btn" onclick="setCmd('COMMIT USUARIO:user MESSAGE:&quot;msg&quot;')">COMMIT</button>
<button class="btn btn-secondary" onclick="setCmd('LOGS')">LOGS</button>
<button class="btn btn-secondary" onclick="setCmd('STATUS')">STATUS</button>
</div>
<button class="btn btn-success" style="width:100%;padding:20px;font-size:1.2em" onclick="executeCommand()">Execute Command</button>
</div>
</div>

<div id="tab-repo" class="tab-content hidden">
<div class="grid">
<div class="card">
<h3>Create Commit</h3>
<div class="input-group"><input type="text" id="commitUser" placeholder="Username"></div>
<div class="input-group"><input type="text" id="commitMessage" placeholder="Commit message"></div>
<button class="btn" onclick="createCommit()">Create Commit</button>
</div>
<div class="card">
<h3>Repository Info</h3>
<div id="repoInfo" style="margin-top:15px">Load repository data...</div>
</div>
</div>
</div>

<div id="tab-files" class="tab-content hidden">
<div class="grid">
<div class="card">
<h3>Upload File</h3>
<div class="input-group"><input type="text" id="fileName" placeholder="Filename"></div>
<div class="input-group"><textarea id="fileContent" rows="5" placeholder="File content..."></textarea></div>
<button class="btn" onclick="uploadFile()">Upload</button>
</div>
<div class="card">
<h3>Download File</h3>
<div class="input-group"><input type="text" id="downloadFile" placeholder="Filename"></div>
<button class="btn" onclick="downloadFile()">Download</button>
<div id="fileDownload" style="margin-top:15px;padding:15px;background:rgba(0,0,0,0.3);border-radius:10px;max-height:300px;overflow:auto;display:none"></div>
</div>
</div>
</div>

<div id="tab-api" class="tab-content hidden">
<div class="card">
<h3>API Key Management</h3>
<button class="btn" onclick="generateAPIKey()">Generate New API Key</button>
<div id="apiKeyDisplay" style="margin-top:20px;padding:20px;background:rgba(0,255,0,0.1);border:2px solid #4ade80;border-radius:10px;display:none">
<strong style="color:#4ade80">Your API Key:</strong>
<div id="apiKeyValue" style="margin-top:10px;padding:15px;background:rgba(0,0,0,0.5);border-radius:5px;font-family:monospace;word-break:break-all"></div>
</div>
</div>
</div>

<div id="tab-stats" class="tab-content hidden">
<div class="grid" id="statsGrid"><div class="card"><h3>Loading...</h3></div></div>
</div>

<div id="tab-logs" class="tab-content hidden">
<div class="card">
<h3>Audit Logs</h3>
<div id="logsDisplay" style="max-height:500px;overflow:auto;margin-top:15px"></div>
</div>
</div>

<div id="response" class="response"></div>
</div>

<footer>
<p>Nexus Platform v{VERSION} | Sovereign Technology</p>
<p>🔒 AES-256-GCM Encryption | Argentina + China</p>
</footer>
</div>

<script>
let currentToken = null, currentUser = null, currentRole = null;

function showTab(tab){{
    document.querySelectorAll('.tab-content').forEach(t=>t.classList.add('hidden'));
    document.querySelectorAll('.nav-tab').forEach(t=>t.classList.remove('active'));
    document.getElementById('tab-'+tab).classList.remove('hidden');
    event.target.classList.add('active');
    if(tab==='stats') loadStats();
    if(tab==='logs') loadLogs();
    if(tab==='repo') loadRepo();
}}

function setCmd(cmd){{document.getElementById('command').value=cmd;document.getElementById('command').focus()}}

function showResponse(data, isError=false){{
    const r=document.getElementById('response');
    r.style.display='block';
    r.textContent=JSON.stringify(data,null,2);
    r.className='response '+(isError?'error':'success');
    r.scrollIntoView({{behavior:'smooth',block:'center'}});
}}

async function api(endpoint,data={{}}){{
    try{{
        const res=await fetch(endpoint,{{method:'POST',headers:{{'Content-Type':'application/json','Authorization':currentToken?`Bearer ${{currentToken}}`:''}},body:JSON.stringify(data)}});
        return await res.json();
    }}catch(e){{return {{estado:'error',mensaje:'Connection error: '+e.message}};}}
}}

async function doLogin(){{
    const user=document.getElementById('loginUser').value.trim();
    const pass=document.getElementById('loginPass').value;
    if(!user || !pass){{showResponse({{error:'Username and password required'}},true);return}}
    const res=await api('/api/login',{{username:user,password:pass}});
    if(res.estado==='exito'){{
        currentToken=generar_token();
        currentUser=user;
        currentRole=res.role||'user';
        document.getElementById('currentUser').textContent=user;
        document.getElementById('userRole').textContent=currentRole.toUpperCase();
        document.getElementById('authPanel').classList.add('hidden');
        document.getElementById('mainPanel').classList.remove('hidden');
        showResponse(res);
    }}else{{showResponse(res,true);}}
}}

async function doRegister(){{
    const user=document.getElementById('regUser').value.trim();
    const pass=document.getElementById('regPass').value;
    if(!user || !pass){{showResponse({{error:'Username and password required'}},true);return}}
    const res=await api('/api/register',{{username:user,password:pass}});
    showResponse(res);
    if(res.estado==='exito'){{setTimeout(()=>{{document.getElementById('loginUser').value=user;alert('User created! Please login.');}},500);}}
}}

function doLogout(){{
    currentToken=null;currentUser=null;currentRole=null;
    document.getElementById('authPanel').classList.remove('hidden');
    document.getElementById('mainPanel').classList.add('hidden');
    document.getElementById('loginUser').value='';
    document.getElementById('loginPass').value='';
    document.getElementById('response').style.display='none';
}}

async function executeCommand(){{
    const cmd=document.getElementById('command').value.trim();
    if(!cmd){{showResponse({{error:'Enter a command'}},true);return}}
    const res=await api('/api/nexus',{{comando_nexus:cmd}});
    showResponse(res);
}}

async function createCommit(){{
    const user=document.getElementById('commitUser').value.trim();
    const msg=document.getElementById('commitMessage').value.trim();
    if(!user || !msg){{showResponse({{error:'Username and message required'}},true);return}}
    const res=await api('/api/nexus',{{comando_nexus:`COMMIT USUARIO:${{user}} MESSAGE:"${{msg}}"`}});
    showResponse(res);
}}

async function uploadFile(){{
    const name=document.getElementById('fileName').value.trim();
    const content=document.getElementById('fileContent').value;
    if(!name){{showResponse({{error:'Filename required'}},true);return}}
    const res=await api('/api/file',{{action:'upload',filename:name,content}});
    showResponse(res);
}}

async function downloadFile(){{
    const name=document.getElementById('downloadFile').value.trim();
    if(!name){{showResponse({{error:'Filename required'}},true);return}}
    const res=await api('/api/file',{{action:'download',filename:name}});
    if(res.estado==='exito'){{document.getElementById('fileDownload').textContent=res.content;document.getElementById('fileDownload').style.display='block';}}
    showResponse(res);
}}

async function generateAPIKey(){{
    const res=await api('/api/apikey');
    if(res.estado==='exito'){{document.getElementById('apiKeyValue').textContent=res.api_key;document.getElementById('apiKeyDisplay').style.display='block';}}
    showResponse(res);
}}

async function loadStats(){{
    const res=await api('/api/stats');
    if(res.estado==='exito' && res.stats){{
        let html='';
        if(res.stats.users) html+=`<div class="card"><h3>Total Users</h3><div class="stat">${{res.stats.users}}</div></div>`;
        if(res.stats.total_data!==undefined) html+=`<div class="card"><h3>Data Size</h3><div class="stat">${{(res.stats.total_data/1024).toFixed(2)}} KB</div></div>`;
        if(res.stats.backups!==undefined) html+=`<div class="card"><h3>Backups</h3><div class="stat">${{res.stats.backups}}</div></div>`;
        if(res.stats.api_keys!==undefined) html+=`<div class="card"><h3>API Keys</h3><div class="stat">${{res.stats.api_keys}}</div></div>`;
        document.getElementById('statsGrid').innerHTML=html;
    }}
}}

async function loadLogs(){{
    const res=await api('/api/logs');
    if(res.estado==='exito' && res.logs){{
        let html=res.logs.slice(-20).reverse().map(l=>`<div style="padding:15px;margin:10px 0;background:rgba(0,0,0,0.3);border-radius:10px;border-left:3px solid #0072CE"><strong style="color:#0072CE">${{l.event}}</strong> | <strong>${{l.user}}</strong> | <small>${{l.timestamp}}</small><br><span style="color:#aaa">${{l.details||''}}</span></div>`).join('');
        document.getElementById('logsDisplay').innerHTML=html;
    }}
}}

async function loadRepo(){{
    document.getElementById('repoInfo').innerHTML='Loading...';
    const res=await api('/api/repo/info');
    if(res.estado==='exito'){{
        document.getElementById('repoInfo').innerHTML=`<div style="line-height:1.8"><strong>Commits:</strong> ${{res.commits||0}}<br><strong>Last update:</strong> ${{res.last_commit||'Never'}}</div>`;
    }}
}}

function generar_token(){{return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g,function(c){{var r=Math.random()*16|0,v=c=='x'?r:(r&0x3|0x8);return v.toString(16);}});}}

document.addEventListener('DOMContentLoaded',()=>{{setInterval(()=>{{if(currentToken) loadStats();}},10000);}});
</script>
</body>
</html>"""

# ==================== HANDLER ====================
class NexusHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        try:
            data = json.loads(post_data)
            
            if self.path == "/api/register":
                username = data.get("username", "")
                password = data.get("password", "")
                if crear_usuario(username, password):
                    self.send_response(200); self.end_headers()
                    self.wfile.write(json.dumps({"estado": "exito", "mensaje": "User created"}).encode())
                else:
                    self.send_response(400); self.end_headers()
                    self.wfile.write(json.dumps({"estado": "error", "mensaje": "User already exists"}).encode())
            
            elif self.path == "/api/login":
                username = data.get("username", "")
                password = data.get("password", "")
                success, user = verificar_usuario(username, password)
                if success:
                    self.send_response(200); self.end_headers()
                    self.wfile.write(json.dumps({"estado": "exito", "mensaje": "Login successful", "role": user["role"]}).encode())
                else:
                    self.send_response(401); self.end_headers()
                    self.wfile.write(json.dumps({"estado": "error", "mensaje": "Invalid credentials"}).encode())
            
            elif self.path == "/api/nexus":
                comando = data.get("comando_nexus", "")
                resultado = interpretar_nexus_lang(comando)
                self.send_response(200); self.end_headers()
                self.wfile.write(json.dumps(resultado, ensure_ascii=False).encode())
            
            elif self.path == "/api/file":
                action = data.get("action", "")
                filename = data.get("filename", "")
                if action == "upload":
                    content = data.get("content", "")
                    filepath = os.path.join(DIRECTORIO_FILES, filename)
                    with open(filepath, "w", encoding="utf-8") as f: f.write(content)
                    log_event("FILE_UPLOAD", "system", f"File: {filename}")
                    self.send_response(200); self.end_headers()
                    self.wfile.write(json.dumps({"estado": "exito", "mensaje": f"File {filename} uploaded"}).encode())
                elif action == "download":
                    filepath = os.path.join(DIRECTORIO_FILES, filename)
                    if os.path.exists(filepath):
                        with open(filepath, "r", encoding="utf-8") as f: content = f.read()
                        self.send_response(200); self.end_headers()
                        self.wfile.write(json.dumps({"estado": "exito", "mensaje": f"File {filename} downloaded", "content": content}).encode())
                    else:
                        self.send_response(404); self.end_headers()
                        self.wfile.write(json.dumps({"estado": "error", "mensaje": "File not found"}).encode())
            
            elif self.path == "/api/apikey":
                api_key = generar_api_key("user")
                self.send_response(200); self.end_headers()
                self.wfile.write(json.dumps({"estado": "exito", "mensaje": "API key generated", "api_key": api_key}).encode())
            
            elif self.path == "/api/stats":
                stats = {}
                if os.path.exists(ARCHIVO_USUARIOS):
                    with open(ARCHIVO_USUARIOS, "r") as f: stats["users"] = len(json.load(f))
                total_size = sum(os.path.getsize(os.path.join(dirpath, filename)) for dirpath, _, filenames in os.walk(DIRECTORIO_DATOS) for filename in filenames)
                stats["total_data"] = total_size
                stats["backups"] = len(os.listdir(DIRECTORIO_BACKUPS))
                if os.path.exists(ARCHIVO_API_KEYS):
                    with open(ARCHIVO_API_KEYS, "r") as f: stats["api_keys"] = len(json.load(f))
                self.send_response(200); self.end_headers()
                self.wfile.write(json.dumps({"estado": "exito", "mensaje": "Stats retrieved", "stats": stats}).encode())
            
            elif self.path == "/api/logs":
                log_file = os.path.join(DIRECTORIO_LOGS, f"{datetime.now().strftime('%Y%m')}.json")
                if os.path.exists(log_file):
                    with open(log_file, "r") as f: logs = json.load(f)
                    self.send_response(200); self.end_headers()
                    self.wfile.write(json.dumps({"estado": "exito", "mensaje": "Logs retrieved", "logs": logs}).encode())
                else:
                    self.send_response(200); self.end_headers()
                    self.wfile.write(json.dumps({"estado": "exito", "mensaje": "No logs", "logs": []}).encode())
            
            else:
                self.send_response(404); self.end_headers()
        except Exception as e:
            self.send_response(400); self.end_headers()
            self.wfile.write(json.dumps({"estado": "error", "mensaje": str(e)}).encode())

    def log_message(self, format, *args): pass

# ==================== INICIO ====================
if __name__ == "__main__":
    print("="*70)
    print(f"NEXUS PLATFORM v{VERSION} - ENTERPRISE EDITION")
    print("="*70)
    print(" AES-256-GCM ENCRYPTION ACTIVE")
    print("Modules: NexusAuth | NexusBase | NexusLang | NexusRepo")
    print("         NexusFiles | NexusAPI | NexusLogs | NexusStats")
    print("="*70)
    print(f"Server: http://localhost:{PUERTO}")
    print("="*70)
    
    servidor = HTTPServer(('localhost', PUERTO), NexusHandler)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        servidor.shutdown()
