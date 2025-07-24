#!/usr/bin/env python3
"""
Agente Dibuja - ML Enhanced App
Aplicación completa con Machine Learning ligero y local
"""

import os
import sys
import time
import random
import json
from datetime import datetime
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

class MLCanvas:
    """Canvas con análisis ML mejorado"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]
        self.move_history = []
    
    def draw_pixel(self, x: int, y: int, symbol: str):
        """Dibujar un píxel"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = symbol
            self.move_history.append({
                'x': x, 'y': y, 'symbol': symbol,
                'timestamp': datetime.now().isoformat()
            })
    
    def analyze_patterns_ml(self) -> dict:
        """Análisis ML ligero de patrones"""
        patterns = {
            'density': 0.0,
            'symmetry': 0.0,
            'clustering': 0.0,
            'balance': 0.0,
            'edge_preference': 0.0
        }
        
        # Densidad
        total = self.width * self.height
        filled = sum(1 for row in self.grid for cell in row if cell != ' ')
        patterns['density'] = filled / total if total > 0 else 0
        
        # Simetría horizontal
        symmetry_score = 0
        for y in range(self.height):
            for x in range(self.width // 2):
                left = self.grid[y][x] != ' '
                right = self.grid[y][self.width - 1 - x] != ' '
                if left == right:
                    symmetry_score += 1
        patterns['symmetry'] = symmetry_score / (self.width * self.height // 2) if self.width * self.height > 0 else 0
        
        # Clustering
        cluster_score = 0
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                neighbors = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if 0 <= y + dy < self.height and 0 <= x + dx < self.width:
                            if self.grid[y + dy][x + dx] != ' ':
                                neighbors += 1
                if self.grid[y][x] != ' ' and neighbors > 2:
                    cluster_score += 1
        patterns['clustering'] = cluster_score / (self.width * self.height) if self.width * self.height > 0 else 0
        
        # Balance
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
        
        # Preferencia de bordes
        edge_cells = 0
        filled_edges = 0
        for y in range(self.height):
            for x in range(self.width):
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    edge_cells += 1
                    if self.grid[y][x] != ' ':
                        filled_edges += 1
        patterns['edge_preference'] = filled_edges / edge_cells if edge_cells > 0 else 0
        
        return patterns
    
    def get_available_positions(self):
        """Obtener posiciones disponibles"""
        return [(x, y) for y in range(self.height) 
                for x in range(self.width) 
                if self.grid[y][x] == ' ']

class MLEnhancedAgent:
    """Agente con ML ligero"""
    
    def __init__(self, name: str, client, canvas, symbols):
        self.name = name
        self.client = client
        self.canvas = canvas
        self.symbols = symbols
        self.memory = []
        self.learning_rate = 0.1
        self.exploration_rate = 0.3
        
    def score_position(self, x: int, y: int, symbol: str, patterns: dict) -> float:
        """Puntuar una posición basada en análisis ML"""
        score = 0.0
        
        # Factor de densidad - evitar áreas muy llenas o muy vacías
        if patterns['density'] < 0.1:
            # Favorecer centro cuando está vacío
            center_x, center_y = self.canvas.width // 2, self.canvas.height // 2
            distance = abs(x - center_x) + abs(y - center_y)
            max_distance = self.canvas.width + self.canvas.height
            score += 1 - (distance / max_distance)
        elif patterns['density'] > 0.7:
            # Favorecer huecos en canvas lleno
            neighbors = 0
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if 0 <= x + dx < self.canvas.width and 0 <= y + dy < self.canvas.height:
                        if self.canvas.grid[y + dy][x + dx] != ' ':
                            neighbors += 1
            score += 1 - (neighbors / 8)
        
        # Factor de simetría
        symmetry_x = self.canvas.width - 1 - x
        symmetry_score = 0
        if 0 <= symmetry_x < self.canvas.width:
            if self.canvas.grid[y][symmetry_x] != ' ':
                symmetry_score += 0.5
        score += symmetry_score
        
        # Factor de balance
        quadrant = 0
        mid_x, mid_y = self.canvas.width // 2, self.canvas.height // 2
        
        if x < mid_x and y < mid_y:
            quadrant = 0
        elif x >= mid_x and y < mid_y:
            quadrant = 1
        elif x < mid_x and y >= mid_y:
            quadrant = 2
        else:
            quadrant = 3
        
        # Favorecer cuadrantes menos usados
        quadrant_counts = [0, 0, 0, 0]
        for py in range(self.canvas.height):
            for px in range(self.canvas.width):
                if self.canvas.grid[py][px] != ' ':
                    if px < mid_x and py < mid_y:
                        quadrant_counts[0] += 1
                    elif px >= mid_x and py < mid_y:
                        quadrant_counts[1] += 1
                    elif px < mid_x and py >= mid_y:
                        quadrant_counts[2] += 1
                    else:
                        quadrant_counts[3] += 1
        
        if quadrant_counts[quadrant] < max(quadrant_counts):
            score += 0.3
        
        # Añadir exploración
        if random.random() < self.exploration_rate:
            score += random.uniform(-0.1, 0.1)
        
        return max(0, score)
    
    def generate_ml_prompt(self, patterns: dict, turn_number: int) -> str:
        """Generar prompt mejorado con análisis ML"""
        suggestions = []
        
        if patterns['density'] < 0.1:
            suggestions.append("El canvas está muy vacío. Enfócate en crear estructuras centrales.")
        elif patterns['density'] > 0.7:
            suggestions.append("El canvas está lleno. Busca huecos para detalles finales.")
        
        if patterns['symmetry'] < 0.3:
            suggestions.append("Considera crear más simetría en el diseño.")
        elif patterns['symmetry'] > 0.7:
            suggestions.append("El arte tiene buena simetría. Continúa con patrones balanceados.")
        
        if patterns['clustering'] < 0.2:
            suggestions.append("Los símbolos están dispersos. Intenta crear grupos o patrones.")
        elif patterns['clustering'] > 0.6:
            suggestions.append("Hay buen clustering. Añade a los grupos existentes.")
        
        # Decidir símbolo basado en patrones
        symbol_recommendations = []
        if patterns['density'] < 0.3:
            symbol_recommendations = ["█", "▓", "▒"]  # Símbolos densos
        elif patterns['density'] < 0.6:
            symbol_recommendations = ["▒", "░", "•"]  # Símbolos medios
        else:
            symbol_recommendations = ["•", "·", "'"]  # Símbolos ligeros
        
        prompt = f"""
Análisis ML del canvas:
- Densidad: {patterns['density']:.2f}
- Simetría: {patterns['symmetry']:.2f}
- Clustering: {patterns['clustering']:.2f}
- Balance: {patterns['balance']:.2f}

Sugerencias basadas en análisis:
{chr(10).join(f"• {s}" for s in suggestions)}

Símbolos recomendados: {', '.join(symbol_recommendations)}

Responde con JSON: {{"x": int, "y": int, "symbol": str, "reason": str}}
"""
        
        return prompt
    
    def make_ml_move(self, turn_number: int) -> dict:
        """Hacer movimiento mejorado con ML"""
        # Análisis de patrones actuales
        patterns = self.canvas.analyze_patterns_ml()
        
        # Obtener posiciones disponibles
        available_positions = self.canvas.get_available_positions()
        
        if not available_positions:
            return {
                "x": random.randint(0, self.canvas.width - 1),
                "y": random.randint(0, self.canvas.height - 1),
                "symbol": random.choice(self.symbols),
                "reason": "Sin posiciones disponibles"
            }
        
        # Usar ML para elegir mejor posición
        best_score = -1
        best_move = None
        
        for x, y in available_positions:
            for symbol in self.symbols:
                score = self.score_position(x, y, symbol, patterns)
                
                if score > best_score:
                    best_score = score
                    best_move = {
                        "x": x,
                        "y": y,
                        "symbol": symbol,
                        "reason": f"Posición ML evaluada con score {score:.2f}",
                        "ml_analysis": patterns
                    }
        
        # Aplicar el movimiento
        if best_move:
            self.canvas.draw_pixel(best_move['x'], best_move['y'], best_move['symbol'])
            self.memory.append(best_move)
            return best_move
        
        # Fallback
        x, y = random.choice(available_positions)
        symbol = random.choice(self.symbols)
        return {
            "x": x,
            "y": y,
            "symbol": symbol,
            "reason": "Movimiento aleatorio por fallback"
        }

class MLEnhancedApp:
    """Aplicación completa con ML"""
    
    def __init__(self):
        self.console = Console()
        self.canvas = MLCanvas(30, 15)
        self.client = None
        self.agent1 = None
        self.agent2 = None
        
    def clear_screen(self):
        """Limpiar pantalla"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_canvas_ml(self):
        """Mostrar canvas con análisis ML"""
        lines = []
        for row in self.canvas.grid:
            colored_line = ""
            for char in row:
                if char == '█':
                    colored_line += '[bold blue]█[/]'
                elif char == '▓':
                    colored_line += '[bold red]▓[/]'
                elif char == '▒':
                    colored_line += '[bold yellow]▒[/]'
                elif char == '░':
                    colored_line += '[bold green]░[/]'
                elif char != ' ':
                    colored_line += f'[bold cyan]{char}[/]'
                else:
                    colored_line += ' '
            lines.append(colored_line)
        return '\n'.join(lines)
    
    def create_ml_stats_table(self, patterns: dict):
        """Crear tabla de estadísticas ML"""
        table = Table(title="📊 Análisis ML del Canvas")
        
        table.add_column("Métrica", style="cyan")
        table.add_column("Valor", style="magenta")
        table.add_column("Interpretación", style="green")
        
        density_interpret = "Vacío" if patterns['density'] < 0.2 else "Medio" if patterns['density'] < 0.6 else "Lleno"
        symmetry_interpret = "Asimétrico" if patterns['symmetry'] < 0.3 else "Simétrico"
        clustering_interpret = "Disperso" if patterns['clustering'] < 0.2 else "Agrupado"
        balance_interpret = "Desbalanceado" if patterns['balance'] < 0.5 else "Balanceado"
        
        table.add_row("Densidad", f"{patterns['density']:.2f}", density_interpret)
        table.add_row("Simetría", f"{patterns['symmetry']:.2f}", symmetry_interpret)
        table.add_row("Clustering", f"{patterns['clustering']:.2f}", clustering_interpret)
        table.add_row("Balance", f"{patterns['balance']:.2f}", balance_interpret)
        
        return table
    
    def run_ml_enhanced_session(self, turns=20):
        """Ejecutar sesión mejorada con ML"""
        self.clear_screen()
        
        # Banner
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                    🤖 AGENTE DIBUJA ML                     ║
║              Machine Learning + Arte ASCII                  ║
║                    Inteligencia Local                     ║
╚══════════════════════════════════════════════════════════════╝
        """
        
        self.console.print(Panel(banner, style="bold magenta"))
        
        # Conectar a LM Studio
        self.console.print("[yellow]🔗 Conectando a LM Studio...[/]")
        try:
            self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
            self.console.print("[green]✅ LM Studio conectado[/]")
        except Exception as e:
            self.console.print(f"[red]❌ Error: {e}[/]")
            return
        
        # Crear agentes ML
        symbols = ["█", "▓", "▒", "░", "▄", "▀", "▌", "▐", "•", "+", "■", "◆"]
        self.agent1 = MLEnhancedAgent("🤖 ML_Agent_1", self.client, self.canvas, symbols)
        self.agent2 = MLEnhancedAgent("🧠 ML_Agent_2", self.client, self.canvas, symbols)
        
        self.console.print("[cyan]⚙️ Inicializando ML...[/]")
        
        for turn in range(turns):
            agent = self.agent1 if turn % 2 == 0 else self.agent2
            agent_name = self.agent1.name if turn % 2 == 0 else self.agent2.name
            
            # Análisis ML antes del movimiento
            patterns = self.canvas.analyze_patterns_ml()
            
            # Movimiento ML mejorado
            move = agent.make_ml_move(turn)
            
            self.clear_screen()
            
            # Mostrar información
            self.console.print(Panel(banner, style="bold magenta"))
            
            # Canvas actual
            canvas_display = self.display_canvas_ml()
            self.console.print(Panel(canvas_display, title=f"🎨 Turno {turn + 1} - {agent_name}"))
            
            # Estadísticas ML
            stats_table = self.create_ml_stats_table(patterns)
            self.console.print(stats_table)
            
            # Información del movimiento
            info_text = f"✏️ Símbolo: '{move['symbol']}'\n📍 Posición: ({move['x']}, {move['y']})\n💭 Razón: {move['reason']}"
            self.console.print(Panel(info_text, title="📋 Decisión ML"))
            
            # Barra de progreso
            progress = (turn + 1) / turns * 100
            bar = "█" * int(progress / 5) + "░" * (20 - int(progress / 5))
            self.console.print(f"📊 Progreso: [{bar}] {progress:.1f}%")
            
            time.sleep(1.5)
        
        # Resultado final
        self.clear_screen()
        final_patterns = self.canvas.analyze_patterns_ml()
        
        self.console.print(Panel(banner, style="bold green"))
        
        final_canvas = self.display_canvas_ml()
        self.console.print(Panel(final_canvas, title="🎨 Arte ML Final"))
        
        self.console.print(self.create_ml_stats_table(final_patterns))
        
        # Guardar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"arte_ml_{timestamp}"
        
        with open(f"{filename}.txt", 'w', encoding='utf-8') as f:
            f.write("=== ARTE ASCII CON ML ===\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            f.write('\n'.join([''.join(row) for row in self.canvas.grid]))
            f.write("\n\n📊 Análisis ML:\n")
            for key, value in final_patterns.items():
                f.write(f"{key}: {value:.3f}\n")
        
        self.console.print(f"[green]✅ Arte ML guardado en {filename}.txt[/]")

if __name__ == "__main__":
    app = MLEnhancedApp()
    
    try:
        app.run_ml_enhanced_session(turns=15)
    except KeyboardInterrupt:
        print("\n[red]⏹️ ML interrumpido[/]")
    except Exception as e:
        print(f"\n[red]❌ Error ML: {e}[/]")
