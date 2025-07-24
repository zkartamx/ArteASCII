#!/bin/bash

# Script de configuración de entorno virtual para Agente Dibuja
# Este script configura tanto entorno virtual como Docker

set -e

echo "🚀 Configurando Agente Dibuja..."
echo "================================="

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $PYTHON_VERSION detectado"

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Verificar que funciona
echo "🔍 Verificando instalación..."
python -c "import config; print('✅ Configuración válida')"
python -c "from canvas import Canvas; c = Canvas(5,5); print('✅ Canvas funciona')"

# Crear directorios necesarios
mkdir -p outputs

# Verificar Docker
echo "🐳 Verificando Docker..."
if command -v docker &> /dev/null; then
    echo "✅ Docker está disponible"
    
    # Verificar Docker Compose
    if command -v docker-compose &> /dev/null; then
        echo "✅ Docker Compose está disponible"
    else
        echo "⚠️  Docker Compose no encontrado. Instálalo con:"
        echo "   pip install docker-compose"
    fi
else
    echo "⚠️  Docker no está instalado"
fi

# Verificar LM Studio
echo "🔍 Verificando LM Studio..."
if curl -s http://localhost:1234/v1/models > /dev/null 2>&1; then
    echo "✅ LM Studio está ejecutándose"
else
    echo "⚠️  LM Studio no está respondiendo"
    echo "   1. Abre LM Studio"
    echo "   2. Carga un modelo"
    echo "   3. Inicia el servidor local"
fi

echo ""
echo "🎉 Configuración completada!"
echo ""
echo "📋 Opciones de ejecución:"
echo "  Local con venv: source .venv/bin/activate && python main.py"
echo "  Local con make: make run"
echo "  Docker: make run-docker"
echo "  Docker Compose: docker-compose up"
echo ""
echo "📁 Archivos generados:"
echo "  - Entorno virtual: .venv/"
echo "  - Outputs: outputs/"
echo "  - Configuración: .env"
