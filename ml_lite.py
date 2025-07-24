#!/usr/bin/env python3
"""
Agente Dibuja - ML Lite
Machine Learning ligero y local para mejorar la inteligencia de los agentes
"""

import json
import random
import math
from typing import Dict, List, Any
from collections import defaultdict, deque

class MLLiteAgent:
    """Agente con ML ligero para mejorar decisiones"""
    
    def __init__(self, name: str):
        self.name = name
        self.memory = deque(maxlen=100)  # Memoria de corto plazo
        self.patterns = defaultdict(int)  # Contador de patrones
        self.style_weights = {
            'minimalista': 0.3,
            'expresivo': 0.3,
            'geometrico': 0.2,
            'organico': 0.2
        }
        self.learning_rate = 0.1
        self.exploration_rate = 0.3
        
    def analyze_canvas_patterns(self, canvas) -> Dict[str, float]:
        """Análisis ligero de patrones en el canvas"""
        patterns = {
            'density': 0.0,
            'symmetry': 0.0,
            'clustering': 0.0,
            'edge_preference': 0.0
        }
        
        # Calcular densidad
        total_cells = canvas.width * canvas.height
        filled_cells = sum(1 for row in canvas.grid for cell in row if cell != ' ')
        patterns['density'] = filled_cells / total_cells
        
        # Calcular simetría horizontal
        symmetry_score = 0
        for y in range(canvas.height):
            for x in range(canvas.width // 2):
                left = canvas.grid[y][x] != ' '
                right = canvas.grid[y][canvas.width - 1 - x] != ' '
                if left == right:
                    symmetry_score += 1
        patterns['symmetry'] = symmetry_score / (canvas.width * canvas.height // 2)
        
        # Calcular clustering
        cluster_score = 0
        for y in range(1, canvas.height - 1):
            for x in range(1, canvas.width - 1):
                neighbors = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if canvas.grid[y + dy][x + dx] != ' ':
                            neighbors += 1
                if canvas.grid[y][x] != ' ' and neighbors > 2:
                    cluster_score += 1
        patterns['clustering'] = cluster_score / (canvas.width * canvas.height)
        
        # Calcular preferencia de bordes
        edge_cells = 0
        filled_edges = 0
        for y in range(canvas.height):
            for x in range(canvas.width):
                if x == 0 or x == canvas.width - 1 or y == 0 or y == canvas.height - 1:
                    edge_cells += 1
                    if canvas.grid[y][x] != ' ':
                        filled_edges += 1
        patterns['edge_preference'] = filled_edges / edge_cells if edge_cells > 0 else 0
        
        return patterns
    
    def score_position(self, x: int, y: int, canvas, symbol: str, patterns: Dict[str, float]) -> float:
        """Puntuar una posición basada en patrones y estilo"""
        score = 0.0
        
        # Factor de cercanía al centro
        center_x, center_y = canvas.width // 2, canvas.height // 2
        distance_to_center = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
        max_distance = math.sqrt(center_x ** 2 + center_y ** 2)
        center_factor = 1 - (distance_to_center / max_distance)
        
        # Factor de cercanía a otros símbolos
        proximity_factor = 0
        neighbors = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < canvas.width and 0 <= ny < canvas.height:
                    if canvas.grid[ny][nx] != ' ':
                        neighbors += 1
        proximity_factor = neighbors / 8
        
        # Factor de simetría
        symmetry_x = canvas.width - 1 - x
        symmetry_factor = 1 if canvas.grid[y][symmetry_x] != ' ' else 0
        
        # Combinar factores basados en estilo actual
        if self.style_weights['minimalista'] > 0.5:
            score = center_factor * 0.3 + (1 - proximity_factor) * 0.7
        elif self.style_weights['expresivo'] > 0.5:
            score = center_factor * 0.7 + proximity_factor * 0.3
        elif self.style_weights['geometrico'] > 0.5:
            score = symmetry_factor * 0.6 + center_factor * 0.4
        else:  # orgánico
            score = proximity_factor * 0.5 + center_factor * 0.5
        
        return score
    
    def learn_from_move(self, move: Dict[str, Any], success: bool):
        """Aprender de un movimiento exitoso o fallido"""
        self.memory.append(move)
        
        # Actualizar pesos de estilo basado en el éxito
        if success:
            # Reforzar el estilo que llevó al éxito
            for style in self.style_weights:
                if style in move.get('reason', '').lower():
                    self.style_weights[style] += self.learning_rate
        else:
            # Reducir el estilo que llevó al fracaso
            for style in self.style_weights:
                if style in move.get('reason', '').lower():
                    self.style_weights[style] -= self.learning_rate * 0.5
        
        # Normalizar pesos
        total = sum(self.style_weights.values())
        for style in self.style_weights:
            self.style_weights[style] = max(0.1, self.style_weights[style] / total)
    
    def generate_smart_prompt(self, canvas, turn_number: int, patterns: Dict[str, float]) -> str:
        """Generar prompt inteligente basado en análisis"""
        
        # Decidir estrategia basada en patrones actuales
        strategy = ""
        
        if patterns['density'] < 0.2:
            strategy = "El canvas está muy vacío. Enfócate en crear estructuras o patrones iniciales."
        elif patterns['density'] > 0.6:
            strategy = "El canvas está lleno. Busca huecos o añade detalles finales."
        elif patterns['symmetry'] > 0.5:
            strategy = "Hay buena simetría. Continúa con patrones simétricos."
        elif patterns['clustering'] > 0.5:
            strategy = "Hay buen clustering. Añade a los grupos existentes o crea nuevos."
        else:
            strategy = "El canvas tiene distribución aleatoria. Intenta crear cohesión."
        
        # Decidir símbolo basado en preferencias aprendidas
        symbol_preferences = {
            'minimalista': ['░', '·'],
            'expresivo': ['█', '▓'],
            'geometrico': ['■', '□', '▲'],
            'organico': ['•', '◦', '~']
        }
        
        dominant_style = max(self.style_weights, key=self.style_weights.get)
        preferred_symbols = symbol_preferences.get(dominant_style, ['█', '▓', '▒', '░'])
        
        prompt = f"""
Análisis del canvas:
- Densidad actual: {patterns['density']:.2f}
- Simetría: {patterns['symmetry']:.2f}
- Clustering: {patterns['clustering']:.2f}
- Preferencia de bordes: {patterns['edge_preference']:.2f}

{strategy}

Basado en tu estilo {dominant_style}, considera usar símbolos como: {', '.join(preferred_symbols)}

Responde con JSON válido: {{"x": int, "y": int, "symbol": str, "reason": str}}
"""
        
        return prompt
    
    def predict_next_move(self, canvas, available_positions: List[tuple]) -> Dict[str, Any]:
        """Predecir el siguiente movimiento basado en ML"""
        patterns = self.analyze_canvas_patterns(canvas)
        
        # Evaluar todas las posiciones disponibles
        best_score = -1
        best_move = None
        
        for x, y in available_positions:
            for symbol in ['█', '▓', '▒', '░', '▄', '▀']:
                score = self.score_position(x, y, canvas, symbol, patterns)
                
                # Añadir factor de exploración
                if random.random() < self.exploration_rate:
                    score += random.uniform(-0.1, 0.1)
                
                if score > best_score:
                    best_score = score
                    best_move = {
                        "x": x,
                        "y": y,
                        "symbol": symbol,
                        "reason": f"Posición evaluada con score {score:.2f} basado en patrones actuales",
                        "ml_score": score
                    }
        
        return best_move
    
    def get_personality_summary(self) -> str:
        """Obtener resumen de la personalidad actual"""
        dominant = max(self.style_weights, key=self.style_weights.get)
        return f"Estilo dominante: {dominant} (peso: {self.style_weights[dominant]:.2f})"

class MLCanvas:
    """Canvas mejorado con análisis ML"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]
        self.move_history = []
        self.pattern_cache = {}
    
    def analyze_patterns_ml(self) -> Dict[str, float]:
        """Análisis ML mejorado de patrones"""
        cache_key = str(self.grid)
        if cache_key in self.pattern_cache:
            return self.pattern_cache[cache_key]
        
        patterns = {
            'density': 0.0,
            'symmetry': 0.0,
            'clustering': 0.0,
            'edge_preference': 0.0,
            'gradient_flow': 0.0,
            'balance': 0.0
        }
        
        # Densidad
        total = self.width * self.height
        filled = sum(1 for row in self.grid for cell in row if cell != ' ')
        patterns['density'] = filled / total
        
        # Simetría
        symmetry_score = 0
        for y in range(self.height):
            for x in range(self.width // 2):
                left = self.grid[y][x] != ' '
                right = self.grid[y][self.width - 1 - x] != ' '
                if left == right:
                    symmetry_score += 1
        patterns['symmetry'] = symmetry_score / (self.width * self.height // 2)
        
        # Balance de distribución
        quadrants = [0, 0, 0, 0]  # TL, TR, BL, BR
        mid_x, mid_y = self.width // 2, self.height // 2
        
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] != ' ':
                    if x < mid_x and y < mid_y:
                        quadrants[0] += 1
                    elif x >= mid_x and y < mid_y:
                        quadrants[1] += 1
                    elif x < mid_x and y >= mid_y:
                        quadrants[2] += 1
                    else:
                        quadrants[3] += 1
        
        patterns['balance'] = 1 - (max(quadrants) - min(quadrants)) / max(quadrants) if max(quadrants) > 0 else 0
        
        self.pattern_cache[cache_key] = patterns
        return patterns
    
    def get_ml_suggestions(self) -> List[str]:
        """Sugerencias ML para mejorar el arte"""
        patterns = self.analyze_patterns_ml()
        suggestions = []
        
        if patterns['density'] < 0.1:
            suggestions.append("El canvas está muy vacío. Añade símbolos en el centro.")
        elif patterns['density'] > 0.8:
            suggestions.append("El canvas está lleno. Busca huecos para detalles.")
        
        if patterns['symmetry'] < 0.3:
            suggestions.append("Considera crear más simetría en el diseño.")
        
        if patterns['balance'] < 0.5:
            suggestions.append("El arte está desequilibrado. Distribuye los símbolos.")
        
        return suggestions

class MLEnhancedAgent:
    """Agente mejorado con ML ligero"""
    
    def __init__(self, name: str, client, canvas, symbols):
        self.name = name
        self.client = client
        self.canvas = canvas
        self.symbols = symbols
        self.ml_agent = MLLiteAgent(name)
        self.memory = []
        
    def make_ml_enhanced_move(self, turn_number: int) -> Dict[str, Any]:
        """Hacer movimiento mejorado con ML"""
        # Análisis de patrones actuales
        patterns = self.canvas.analyze_patterns_ml()
        
        # Generar prompt inteligente
        prompt = self.ml_agent.generate_smart_prompt(self.canvas, turn_number, patterns)
        
        # Usar ML para predecir mejor posición
        available_positions = [(x, y) for y in range(self.canvas.height) 
                              for x in range(self.canvas.width) 
                              if self.canvas.grid[y][x] == ' ']
        
        if available_positions:
            # Usar ML para elegir la mejor posición
            best_move = self.ml_agent.predict_next_move(self.canvas, available_positions)
            
            # Aplicar el movimiento
            self.canvas.draw_pixel(best_move['x'], best_move['y'], best_move['symbol'])
            
            # Aprender del movimiento
            self.ml_agent.learn_from_move(best_move, success=True)
            
            return best_move
        
        return {
            "x": random.randint(0, self.canvas.width - 1),
            "y": random.randint(0, self.canvas.height - 1),
            "symbol": random.choice(self.symbols),
            "reason": "Sin posiciones disponibles - movimiento aleatorio"
        }

# Ejemplo de uso
if __name__ == "__main__":
    print("🤖 ML Lite - Agente Dibuja Mejorado")
    print("=" * 50)
    
    # Crear agente ML
    ml_agent = MLLiteAgent("Test_Agent")
    
    # Ejemplo de análisis
    from sync_agent import SyncCanvas
    
    canvas = SyncCanvas(10, 5)
    canvas.draw_pixel(2, 2, '█')
    canvas.draw_pixel(3, 2, '▓')
    
    patterns = ml_agent.analyze_canvas_patterns(canvas)
    print("📊 Patrones detectados:")
    for pattern, value in patterns.items():
        print(f"   {pattern}: {value:.3f}")
    
    print(f"\n🎭 Personalidad: {ml_agent.get_personality_summary()}")
    
    suggestions = canvas.get_ml_suggestions()
    print("\n💡 Sugerencias ML:")
    for suggestion in suggestions:
        print(f"   • {suggestion}")
