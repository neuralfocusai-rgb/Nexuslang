#!/bin/bash
echo "🌐 Installing NexusLang v5.3..."
mkdir -p ~/.nexuslang
curl -sSL https://raw.githubusercontent.com/neuralfocusai-rgb/Nexuslang/main/nexuslang.py -o ~/.nexuslang/nexuslang.py
printf '#!/bin/bash\npython3 ~/.nexuslang/nexuslang.py "$@"\n' > ~/.nexuslang/nexus
chmod +x ~/.nexuslang/nexus
echo 'export PATH="$HOME/.nexuslang:$PATH"' >> ~/.bashrc
echo "✅ Listo! Reinicia la terminal y escribe: nexus --demo"
