#!/usr/bin/env python3
"""
SCRIPT DE REORGANIZACIÓN AUTOMÁTICA
Optimiza la estructura del proyecto para GitHub
"""

import os
import shutil
import glob
from pathlib import Path

def reorganize_project():
    print("🎯 Reorganizando proyecto ArteASCII...")
    
    # Crear estructura optimizada
    structure = {
        'src/': ['genetic/', 'quantum/', 'diverse/', 'master/'],
        'outputs/': ['genetic/', 'quantum/', 'diverse/', 'master/'],
        'examples/': [],
        'docs/': [],
        'scripts/': []
    }
    
    # Crear directorios
    for main_dir, sub_dirs in structure.items():
        os.makedirs(main_dir, exist_ok=True)
        for sub_dir in sub_dirs:
            os.makedirs(os.path.join(main_dir, sub_dir), exist_ok=True)
    
    # Organizar archivos principales
    organized_files = {
        'genetic': [
            'creaciones_lm_studio/genetico/lm_studio_genetic_complete.py',
            'creaciones_lm_studio/genetico/lm_studio_genetic_organizer.py',
            'creaciones_lm_studio/genetico/lm_studio_genetic_visual.py'
        ],
        'quantum': [
            'creaciones_lm_studio/cuantico/lm_studio_quantum_complete.py',
            'creaciones_lm_studio/cuantico/lm_studio_quantum_organizer.py',
            'creaciones_lm_studio/cuantico/lm_studio_quantum_visual.py'
        ],
        'diverse': [
            'creaciones_lm_studio/diversidad/lm_studio_diverse_complete.py',
            'creaciones_lm_studio/diversidad/lm_studio_diverse_organizer.py',
            'creaciones_lm_studio/diversidad/lm_studio_diverse_visual.py'
        ],
        'master': [
            'creaciones_lm_studio/artefinal/lm_studio_master_complete.py',
            'creaciones_lm_studio/artefinal/lm_studio_master_organizer.py',
            'creaciones_lm_studio/artefinal/lm_studio_master_visual.py'
        ]
    }
    
    # Copiar archivos organizados
    for system, files in organized_files.items():
        for file_path in files:
            if os.path.exists(file_path):
                dest = f"src/{system}/"
                shutil.copy2(file_path, dest)
                print(f"✅ {file_path} → {dest}")
    
    # Organizar outputs
    output_mapping = {
        'genetic': 'creaciones_lm_studio/genetico/*.json',
        'quantum': 'creaciones_lm_studio/cuantico/*.json',
        'diverse': 'creaciones_lm_studio/diversidad/*.json',
        'master': 'creaciones_lm_studio/artefinal/*.json'
    }
    
    for system, pattern in output_mapping.items():
        for file_path in glob.glob(pattern):
            if os.path.exists(file_path):
                dest = f"outputs/{system}/"
                shutil.copy2(file_path, dest)
                print(f"✅ {file_path} → {dest}")
    
    # Crear README optimizado
    readme_content = """# 🎨 ArteASCII - Sistema Multi-Agente con LM Studio

## 📂 Estructura Optimizada

```
ArteASCII/
├── 📁 src/                    # Código fuente organizado
│   ├── 📁 genetic/           # Sistema genético
│   ├── 📁 quantum/           # Sistema cuántico
│   ├── 📁 diverse/           # Sistema diverso
│   └── 📁 master/            # Sistema master
├── 📁 outputs/               # Salidas organizadas
├── 📁 examples/              # Ejemplos
├── 📁 docs/                  # Documentación
└── 📁 scripts/               # Utilidades
```

## 🚀 Uso Rápido

```bash
# Ejecutar sistema genético
python src/genetic/lm_studio_genetic_complete.py

# Ejecutar sistema cuántico
python src/quantum/lm_studio_quantum_complete.py

# Ejecutar sistema diverso
python src/diverse/lm_studio_diverse_complete.py

# Ejecutar master completo
python src/master/lm_studio_master_complete.py
```

## 📊 Características

- ✅ Arte ASCII completo en JSON
- ✅ Decisiones reales de LM Studio
- ✅ Organización por carpetas claras
- ✅ Scripts ejecutables
- ✅ Documentación centralizada
"""
    
    with open('README_OPTIMIZED.md', 'w') as f:
        f.write(readme_content)
    
    print("\n🎯 Reorganización completa!")
    print("📁 Estructura optimizada creada")
    print("✅ Archivos organizados por sistema")
    print("🚀 Lista para GitHub")

if __name__ == "__main__":
    reorganize_project()
