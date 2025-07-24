# 🧠 Información del Modelo - Agente Dibuja

## 📋 Modelo Actual

### 🎯 **Modelo en Uso: LM Studio Local**
- **URL**: `http://localhost:1234/v1`
- **Tipo**: Local LLM via LM Studio
- **Proveedor**: OpenAI-compatible API (LM Studio)

### 🔧 **Configuración Actual**
```python
# En todos los archivos
client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="not-needed"  # LM Studio no requiere API key local
)
```

### 📊 **Modelos Recomendados para LM Studio**

#### **Modelos Optimizados para Arte ASCII**
1. **Llama 2 7B Chat** - Balance rendimiento/calidad
2. **CodeLlama 7B** - Excelente para código/estructuras
3. **Mistral 7B Instruct** - Respuestas creativas
4. **Phi-2** - Ligero y eficiente

#### **Instalación en LM Studio**
1. Abrir LM Studio
2. Ir a "Discover" o "Download Models"
3. Buscar: `llama-2-7b-chat` o `mistral-7b-instruct`
4. Descargar y cargar el modelo
5. Verificar en: `http://localhost:1234`

### 🚀 **Cómo Cambiar el Modelo**

#### **Opción 1: Cambiar en config.py**
```python
# config.py
LM_STUDIO_URL = "http://localhost:1234/v1"
# Cambiar a otro puerto si es necesario
# LM_STUDIO_URL = "http://localhost:8080/v1"
```

#### **Opción 2: Modelos Alternativos**
```python
# Para usar OpenAI real (requiere API key)
# client = OpenAI(api_key="sk-...")

# Para usar Ollama
# client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# Para usar diferentes modelos locales
# client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
```

### 📈 **Modelos Compatibles**

#### **Local Models (LM Studio)**
- ✅ **Llama 2** (7B, 13B)
- ✅ **CodeLlama** (7B, 13B)
- ✅ **Mistral** (7B)
- ✅ **Phi-2** (2.7B)
- ✅ **Gemma** (7B)

#### **Características del Modelo Actual**
- **Contexto**: 4K-8K tokens
- **Respuesta**: JSON válido
- **Creatividad**: Alta para arte ASCII
- **Rendimiento**: Local y rápido

### 🔍 **Verificar Modelo Actual**

```bash
# Comando para verificar modelo en LM Studio
curl http://localhost:1234/v1/models
```

### 🛠️ **Debugging de Modelo**

```bash
# Verificar si LM Studio está corriendo
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "local-model",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### 📊 **Comparación de Modelos**

| Modelo | Tamaño | Velocidad | Calidad | Uso RAM |
|--------|--------|-----------|---------|---------|
| Llama 2 7B | 7B | Media | Alta | ~6GB |
| Mistral 7B | 7B | Alta | Excelente | ~6GB |
| Phi-2 | 2.7B | Muy Alta | Buena | ~3GB |
| CodeLlama 7B | 7B | Media | Excelente | ~6GB |

### 🎯 **Recomendaciones**

#### **Para Arte ASCII Creativo**
- **Mistral 7B** - Mejor balance creatividad/estructura
- **Llama 2 7B** - Respuestas consistentes

#### **Para Rendimiento Máximo**
- **Phi-2** - Más rápido, menos RAM
- **Gemma 7B** - Optimizado para arte

### 🔧 **Configuración Avanzada**

#### **Personalizar Prompts por Modelo**
```python
# Para modelos más creativos
enhanced_prompt = f"""
Actúa como artista ASCII profesional. Crea arte con estilo único.

Análisis del canvas:
- Densidad: {patterns['density']:.2f}
- Simetría: {patterns['symmetry']:.2f}

Responde con JSON válido: {{"x": int, "y": int, "symbol": str, "reason": str, "style": str}}
"""
```

### 📋 **Resumen del Modelo Actual**
- **Modelo**: LM Studio Local (configurable)
- **API**: OpenAI-compatible
- **Endpoint**: `http://localhost:1234/v1`
- **Key**: No requerida
- **Formato**: JSON responses
- **Optimización**: Arte ASCII multi-agente
