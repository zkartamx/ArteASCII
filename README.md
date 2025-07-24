# 🤖 Agente Dibuja - Arte ASCII Multi-Agente con LM Studio

Un **ecosistema completo** de arte ASCII evolutivo que utiliza **LM Studio** para tomar decisiones creativas en tiempo real. Cada sistema evoluciona arte ASCII basándose en decisiones reales de inteligencia artificial local.

## 🚀 Sistemas LM Studio Activos

### 🧬 **Evolución Genética LM Studio REAL**
- Cada mutación, cruce y selección es decidida por LM Studio
- Decisiones reales sobre: forma, posición, símbolo, complejidad
- Guardado en: `creaciones_lm_studio/genetico/`

### ⚛️ **Evolución Cuántica LM Studio REAL**
- Estados cuánticos (superposición, entrelazamiento, decoherencia) decididos por LM Studio
- Fractales y coherencia cuántica controlados por IA
- Guardado en: `creaciones_lm_studio/cuantico/`

### 🎨 **Diversidad LM Studio REAL**
- Formas únicas y complejas generadas por LM Studio
- Diversidad máxima con decisiones creativas reales
- Guardado en: `creaciones_lm_studio/diversidad/`

## 📁 Estructura de Carpetas Organizadas

```
creaciones_lm_studio/
├── genetico/           # Evolución genética
│   ├── lm_studio_genetic_organizer.py
│   └── genetic_evolution_*.json
├── cuantico/           # Evolución cuántica
│   ├── lm_studio_quantum_organizer.py
│   └── quantum_evolution_*.json
├── diversidad/         # Diversidad máxima
│   ├── lm_studio_diverse_organizer.py
│   └── diverse_artwork_*.json
├── artefinal/          # Sesiones master
│   ├── lm_studio_master_organizer.py
│   └── master_session_*.json
└── 📊 Resultados con analytics completos
```

## 🚀 Instalación y Configuración LM Studio

### 📦 **Instalación Completa**

1. **Dependencias del sistema LM Studio:**
```bash
# Instalar dependencias principales
pip install -r requirements.txt

# Verificar que LM Studio esté activo
python -c "from openai import OpenAI; client = OpenAI(base_url='http://localhost:1234/v1', api_key='not-needed'); print('✅ LM Studio conectado')"
```

2. **Configuración LM Studio:**
   - Descarga [LM Studio](https://lmstudio.ai/)
   - Carga un modelo creativo (Llama 2, Code Llama, etc.)
   - Asegúrate de que el servidor local esté en `http://localhost:1234`
   - El sistema detectará automáticamente si LM Studio está disponible

### 🎮 **Uso de Sistemas LM Studio**

#### **Sistema Individual:**
```bash
# Ejecutar evolución genética
python creaciones_lm_studio/genetico/lm_studio_genetic_organizer.py

# Ejecutar evolución cuántica  
python creaciones_lm_studio/cuantico/lm_studio_quantum_organizer.py

# Ejecutar diversidad máxima
python creaciones_lm_studio/diversidad/lm_studio_diverse_organizer.py
```

#### **Sistema Master (todos juntos):**
```bash
# Ejecutar todos los sistemas
python creaciones_lm_studio/artefinal/lm_studio_master_organizer.py
```

### ⚙️ **Configuración Personalizada**

#### **Archivos de configuración:**
- `creaciones_lm_studio/genetico/lm_studio_genetic_organizer.py` - Configuración genética
- `creaciones_lm_studio/cuantico/lm_studio_quantum_organizer.py` - Configuración cuántica
- `creaciones_lm_studio/diversidad/lm_studio_diverse_organizer.py` - Configuración diversidad

#### **Variables personalizables:**
```python
# En cada sistema:
- CANVAS_WIDTH = 40     # Ancho del canvas ASCII
- CANVAS_HEIGHT = 20    # Alto del canvas ASCII
- GENERATIONS = 5       # Número de generaciones/evoluciones
- SHAPES_COUNT = 12     # Número de formas únicas
- COMPLEXITY_RANGE = (1, 5)  # Rango de complejidad
```

### 📊 **Analytics y Métricas**

Cada sistema genera:
- **JSON con decisiones de LM Studio** - Timestamp único
- **Métricas de evolución** - Fitness, coherencia, diversidad
- **Arte ASCII final** - Canvas con símbolos únicos
- **Analytics completos** - Estadísticas de cada creación

### 🔄 **Flujo de trabajo:**
1. **LM Studio decide** → Real decisiones creativas
2. **Sistema ejecuta** → Genera arte ASCII
3. **Guarda en carpetas** → Organizado por sistema
4. **Analytics disponibles** → JSON con métricas

### 🎨 **Ejemplos de salida:**
```
🧬 EVOLUCIÓN GENÉTICA COMPLETADA:
- Individuos: 8
- Formas únicas: 3
- LM Studio activo: ✅

⚛️ CUÁNTICO COMPLETADO:
- Estados cuánticos: 8
- Coherencia promedio: 0.514

🎨 DIVERSIDAD COMPLETADA:
- Formas únicas: 10
- Tipos de formas: 7
```

## 📊 **Formato de JSON Output**

Cada creación genera un archivo JSON con estructura:
```json
{
  "lm_studio_genetic_folder": {
    "population": [...],
    "folder": "/path/to/creaciones/",
    "evolution_type": "genetic_lm_studio",
    "timestamp": "20250723_231337"
  }
}
```

## 🎯 **Casos de Uso**

- **Arte generativo** - Crear arte ASCII único
- **Investigación AI** - Estudiar decisiones creativas de LLM
- **Educación** - Demostrar evolución y sistemas complejos
- **Prototipos** - Base para sistemas más complejos

## 🤝 **Contribuciones**

¡Las contribuciones son bienvenidas! Puedes:
- Agregar nuevos sistemas evolutivos
- Mejorar los prompts de LM Studio
- Optimizar los algoritmos
- Agregar nuevas métricas y visualizaciones

## 📈 **Estadísticas de Sesión**

El sistema master genera estadísticas completas:
- Total de decisiones LM Studio
- Diversidad de formas generadas
- Complejidad promedio
- Métricas de evolución
- Tiempos de ejecución

## 🔍 **Debugging y Logs**

Los sistemas incluyen:
- **Logs detallados** de cada decisión de LM Studio
- **Fallback seguro** si LM Studio no está disponible
- **Manejo de errores** robusto
- **Métricas de rendimiento**

## 🌟 **Características Avanzadas**

- **Persistencia completa** - Toda la historia de creaciones
- **Analytics en tiempo real** - Métricas durante la ejecución
- **Sistema modular** - Fácil agregar nuevos tipos de evolución
- **Interfaz Rich** - Consola bonita y informativa
- **JSON estructurado** - Fácil análisis posterior

## 🚀 **Próximos Pasos**
- Sistema web para visualizar creaciones
- Integración con más modelos de LM Studio
- Exportación a formatos adicionales
- Dashboard interactivo de estadísticasAGENT_1_NAME=Agente_Azul  # Nombre del primer agente
AGENT_2_NAME=Agente_Rojo  # Nombre del segundo agente
MAX_TURNS=50             # Máximo de turnos
DELAY_ENTRE_TURNOS=1.0   # Segundos entre turnos

# Configuración LM Studio
LM_STUDIO_BASE_URL=http://localhost:1234/v1
LM_STUDIO_API_KEY=not-needed-for-local
```

## 🎯 Características

- **Canvas dinámico**: Visualización en tiempo real con Rich
- **Estilos únicos**: Cada agente tiene su propio estilo artístico
- **Decisión inteligente**: Usa LLM local para decisiones creativas
- **Persistencia**: Guarda el arte final en archivos de texto
- **Estadísticas**: Análisis detallado del proceso creativo

## 🏗️ Arquitectura

```
Agente_Dibuja/
├── main.py          # Orquestador principal
├── agent.py         # Clase DrawingAgent
├── canvas.py        # Gestión del canvas ASCII
├── config.py        # Configuración centralizada
├── requirements.txt # Dependencias
├── .env.example     # Plantilla de configuración
└── README.md        # Este archivo
```

## 🎨 Ejemplos de Estilos

Los agentes pueden tener diferentes estilos:
- **Minimalista**: Prefiere bordes y líneas simples
- **Expresivo**: Se centra en áreas centrales con alta densidad
- **Geométrico**: Crea patrones estructurados
- **Orgánico**: Flujo natural y curvas

## 📊 Salida

Durante la ejecución verás:
- Canvas actualizado en cada turno
- Decisiones de cada agente con justificación
- Estadísticas en tiempo real
- Archivo final guardado como `arte_ascii_TIMESTAMP.txt`

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Puedes:
- Agregar más agentes
- Implementar nuevos estilos artísticos
- Mejorar los prompts para el LLM
- Agregar nuevos símbolos ASCII
- Implementar modos de colaboración adicionales

## 📄 Licencia

MIT License - siéntete libre de usar y modificar.

---

**Nota**: Asegúrate de tener LM Studio ejecutándose antes de iniciar el proyecto. Si encuentras problemas de conexión, verifica que el servidor esté activo en `http://localhost:1234`.
