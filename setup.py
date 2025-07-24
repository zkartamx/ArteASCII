#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Verificar versión de Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ es requerido")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detectado")

def install_dependencies():
    """Instalar dependencias"""
    print("📦 Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas")
    except subprocess.CalledProcessError:
        print("❌ Error instalando dependencias")
        sys.exit(1)

def check_lm_studio():
    """Verificar conexión con LM Studio"""
    import requests
    try:
        response = requests.get("http://localhost:1234/v1/models", timeout=5)
        if response.status_code == 200:
            print("✅ LM Studio está ejecutándose")
            return True
    except requests.exceptions.RequestException:
        pass
    
    print("⚠️  LM Studio no detectado")
    print("   Por favor:")
    print("   1. Abre LM Studio")
    print("   2. Carga un modelo")
    print("   3. Inicia el servidor local")
    return False

def create_env_file():
    """Crear archivo .env si no existe"""
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creando archivo .env...")
        with open('.env.example', 'r') as source, open('.env', 'w') as target:
            target.write(source.read())
        print("✅ Archivo .env creado - edítalo para personalizar")
    else:
        print("✅ Archivo .env ya existe")

def main():
    """Setup completo del proyecto"""
    print("🚀 Configurando Agente Dibuja...")
    print("=" * 40)
    
    check_python_version()
    install_dependencies()
    create_env_file()
    
    print("\n" + "=" * 40)
    print("📋 Próximos pasos:")
    print("1. Abre LM Studio y carga un modelo")
    print("2. Asegúrate de que el servidor esté en http://localhost:1234")
    print("3. Personaliza .env si lo deseas")
    print("4. Ejecuta: python main.py")
    print("=" * 40)

if __name__ == "__main__":
    main()
