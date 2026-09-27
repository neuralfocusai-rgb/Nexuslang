#!/usr/bin/env bash
set -e
echo "🌀 Installing NexusLang v5.4.0 ..."
python3 -m pip install --upgrade "git+https://github.com/neuralfocusai-rgb/Nexuslang.git"
echo "✅ Listo! Reinicia la terminal y escribe: nexus --demo   o   nexuslang hola_urdu.nx"
