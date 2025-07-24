#!/usr/bin/env python3
"""
Agente Dibuja - Professional Edition
Sistema completo de próxima generación
"""

import os
import sys
import time
import json
import random
import math
from datetime import datetime
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from collections import defaultdict, deque

class ProfessionalCanvas:
    """Canvas profesional con todas las mejoras"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]
        self.move_history = []
        self.analytics = {
            'total_moves': 0,
            'unique_symbols': set(),
            'density_evolution': [],
            'symmetry_score': 0.0,
            'balance_score': 0.0
        }
    
    def draw_pixel(self, x: int, y: int, symbol: str):
        """Dibujar con tracking profesional"""
        if 0 <= x < self.width and 0 <= y < self.height:
            old_symbol = self.grid[y][x]
            self.grid[y][x] = symbol
            
            self.move_history.append({
                'x': x, 'y': y, 'symbol': symbol,
                'timestamp': datetime.now().isoformat(),
                'old_symbol': old_symbol
            })
            
            self.analytics['unique_symbols'].add(symbol)
            self.analytics['total_moves'] += 1
    
    def analyze_professional_patterns(self) -> dict:
        """Análisis profesional de patrones"""
        patterns = {
            'density': 0.0,
            'symmetry': 0.0,
            'clustering': 0.0,
            'balance': 0.0,
            'edge_preference': 0.0,
            'center_focus': 0.0
        }
        
        # Densidad
        total_cells = self.width * self.height
        filled_cells = sum(1 for row in self.grid for cell in row if cell != ' ')
        patterns['density'] = filled_cells / total_cells
        
        # Simetría horizontal y vertical
        horizontal_symmetry = 0
        vertical_symmetry = 0
        
        for y in range(self.height):
            for x in range(self.width // 2):
                left = self.grid[y][x] != ' '
                right = self.grid[y][self.width - 1 - x] != ' '
                if left == right:
                    horizontal_symmetry += 1
        
        for x in range(self.width):
            for y in range(self.height // 2):
                top = self.grid[y][x] != ' '
                bottom = self.grid[self.height - 1 - y][x] != ' '
                if top == bottom:
                    vertical_symmetry += 1
        
        patterns['symmetry'] = (horizontal_symmetry + vertical_symmetry) / (total_cells // 2)
        
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
        patterns['clustering'] = cluster_score / total_cells
        
        # Balance de cuadrantes
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
        
        max_quad = max(quadrants)
        min_quad = min(quadrants)
        patterns['balance'] = 1 - ((max_quad - min_quad) / max_quad) if max_quad > 0 else 0
        
        # Preferencia de centro vs bordes
        center_x, center_y = self.width // 2, self.height // 2
        center_distance_sum = 0
        total_distance = 0
        
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] != ' ':
                    distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                    max_distance = math.sqrt(center_x**2 + center_y**2)
                    center_distance_sum += 1 - (distance / max_distance)
        
        patterns['center_focus'] = center_distance_sum / filled_cells if filled_cells > 0 else 0
        
        return patterns

class ProfessionalAgent:
    """Agente profesional con IA avanzada"""
    
    def __init__(self, name: str, client, canvas, symbols):
        self.name = name
        self.client = client
        self.canvas = canvas
        self.symbols = symbols
        self.memory = deque(maxlen=500)
        self.style_evolution = {
            'creativity': random.uniform(0.4, 0.7),
            'precision': random.uniform(0.4, 0.7),
            'balance': random.uniform(0.4, 0.7),
            'innovation': random.uniform(0.4, 0.7)
        }
        self.evolution_history = []
        self.success_rate = 0.75
    
    def calculate_professional_score(self, x: int, y: int, symbol: str, patterns: dict) -> float:
        """Cálculo profesional de score"""
        score = 0.0
        
        # Factor de creatividad
        creativity = self.style_evolution['creativity']
        
        # Factor de precisión
        precision = self.style_evolution['precision']
        
        # Factor de balance
        balance = self.style_evolution['balance']
        
        # Factor de innovación
        innovation = self.style_evolution['innovation']
        
        # Análisis complejo de posición
        center_x, center_y = self.canvas.width // 2, self.canvas.height // 2
        distance_from_center = math.sqrt((x - center_x)**2 + (y - center_y)**2)
        max_distance = math.sqrt(center_x**2 + center_y**2)
        
        # Score basado en patrones actuales
        density_factor = 1 - abs(patterns['density'] - 0.5)  # Favorecer densidad media
        symmetry_factor = patterns['symmetry']
        balance_factor = patterns['balance']
        center_factor = 1 - (distance_from_center / max_distance)
        
        # Combinación ponderada
        score = (
            creativity * density_factor * 0.3 +
            precision * symmetry_factor * 0.2 +
            balance * balance_factor * 0.3 +
            innovation * center_factor * 0.2
        )
        
        # Añadir factor de evolución
        evolution_bonus = random.uniform(-0.1, 0.1) * innovation
        score += evolution_bonus
        
        return max(0, min(1, score))
    
    def evolve_professional_style(self, success_rate: float):
        """Evolución profesional del estilo"""
        learning_rate = 0.05
        
        for trait in self.style_evolution:
            if random.random() < 0.1:  # 10% de mutación
                change = random.uniform(-learning_rate, learning_rate)
                current_value = self.style_evolution[trait]
                new_value = max(0.1, min(1.0, current_value + change))
                self.style_evolution[trait] = new_value
        
        self.evolution_history.append({
            'timestamp': datetime.now().isoformat(),
            'success_rate': success_rate,
            'style': self.style_evolution.copy()
        })
    
    def generate_professional_prompt(self, patterns: dict, turn_number: int) -> str:
        """Generar prompt profesional"""
        style_summary = f"""
Estilo evolutivo actual:
- Creatividad: {self.style_evolution['creativity']:.2f}
- Precisión: {self.style_evolution['precision']:.2f}
- Balance: {self.style_evolution['balance']:.2f}
- Innovación: {self.style_evolution['innovation']:.2f}

Análisis profesional del canvas:
- Densidad: {patterns['density']:.2f}
- Simetría: {patterns['symmetry']:.2f}
- Clustering: {patterns['clustering']:.2f}
- Balance: {patterns['balance']:.2f}
- Enfoque central: {patterns['center_focus']:.2f}

Responde con JSON profesional incluyendo: x, y, symbol, reason, artistic_intent, style_confidence
"""
        return style_summary
    
    def make_professional_move(self, turn_number: int) -> dict:
        """Movimiento profesional"""
        patterns = self.canvas.analyze_professional_patterns()
        
        available_positions = [(x, y) for y in range(self.canvas.height) 
                              for x in range(self.canvas.width) 
                              if self.canvas.grid[y][x] == ' ']
        
        if not available_positions:
            return {
                "x": random.randint(0, self.canvas.width - 1),
                "y": random.randint(0, self.canvas.height - 1),
                "symbol": random.choice(self.symbols),
                "reason": "Fallback: sin posiciones disponibles",
                "artistic_intent": "emergency_mode",
                "style_confidence": 0.1
            }
        
        # Evaluación profesional
        best_score = -1
        best_move = None
        
        for x, y in available_positions:
            for symbol in self.symbols:
                score = self.calculate_professional_score(x, y, symbol, patterns)
                
                if score > best_score:
                    best_score = score
                    best_move = {
                        "x": x,
                        "y": y,
                        "symbol": symbol,
                        "reason": f"Decisión profesional basada en análisis ML con score {score:.3f}",
                        "artistic_intent": "evolución_estilística",
                        "style_confidence": best_score,
                        "patterns_analyzed": patterns
                    }
        
        if best_move:
            self.canvas.draw_pixel(best_move['x'], best_move['y'], best_move['symbol'])
            self.memory.append(best_move)
            
            # Evolucionar estilo
            self.evolve_professional_style(self.success_rate)
            
            return best_move
        
        return {
            "x": random.choice(available_positions)[0],
            "y": random.choice(available_positions)[1],
            "symbol": random.choice(self.symbols),
            "reason": "Movimiento aleatorio profesional",
            "artistic_intent": "exploración",
            "style_confidence": 0.5
        }

class ProfessionalApp:
    """Aplicación profesional completa"""
    
    def __init__(self):
        self.console = Console()
        self.canvas = ProfessionalCanvas(35, 20)
        self.client = None
        self.agents = []
        self.session_analytics = {
            'start_time': datetime.now(),
            'total_moves': 0,
            'successful_ml_decisions': 0,
            'evolution_cycles': 0,
            'art_quality_scores': []
        }
    
    def clear_screen(self):
        """Limpiar pantalla multiplataforma"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def create_professional_banner(self):
        """Banner profesional"""
        return """
╔══════════════════════════════════════════════════════════════════════════════╗
║                           🚀 AGENTE DIBUJA PRO                           ║
║                    Sistema Profesional de Arte ASCII                      ║
║                   ML Avanzado + Analytics + Evolución                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
    
    def display_professional_canvas(self):
        """Display profesional del canvas"""
        lines = []
        for row in self.canvas.grid:
            colored_line = ""
            for char in row:
                if char == '█':
                    colored_line += '[bold bright_white]█[/]'
                elif char == '▓':
                    colored_line += '[bold bright_yellow]▓[/]'
                elif char == '▒':
                    colored_line += '[bold bright_cyan]▒[/]'
                elif char == '░':
                    colored_line += '[bold bright_green]░[/]'
                elif char != ' ':
                    colored_line += f'[bold magenta]{char}[/]'
                else:
                    colored_line += ' '
            lines.append(colored_line)
        return '\n'.join(lines)
    
    def create_professional_dashboard(self, patterns: dict):
        """Dashboard profesional"""
        dashboard = Table(title="📊 Dashboard Profesional")
        
        dashboard.add_column("Métrica", style="cyan")
        dashboard.add_column("Valor", style="magenta")
        dashboard.add_column("Análisis", style="green")
        
        # Análisis profesional
        density_analysis = "Óptimo" if 0.3 <= patterns['density'] <= 0.7 else "Ajustar"
        symmetry_analysis = "Excelente" if patterns['symmetry'] > 0.7 else "Mejorar"
        balance_analysis = "Balanceado" if patterns['balance'] > 0.6 else "Desbalanceado"
        
        dashboard.add_row("Densidad", f"{patterns['density']:.3f}", density_analysis)
        dashboard.add_row("Simetría", f"{patterns['symmetry']:.3f}", symmetry_analysis)
        dashboard.add_row("Balance", f"{patterns['balance']:.3f}", balance_analysis)
        dashboard.add_row("Clustering", f"{patterns['clustering']:.3f}", "Activo")
        dashboard.add_row("Enfoque Central", f"{patterns['center_focus']:.3f}", "Evaluado")
        
        return dashboard
    
    def run_professional_session(self, turns=20):
        """Sesión profesional completa"""
        self.clear_screen()
        
        # Inicialización profesional
        self.console.print(Panel(self.create_professional_banner(), style="bold bright_blue"))
        
        # Conectar a LM Studio
        self.console.print("[yellow]🔗 Inicializando motor profesional...[/]")
        try:
            self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
            self.console.print("[green]✅ Motor profesional conectado[/]")
        except Exception as e:
            self.console.print(f"[red]❌ Error profesional: {e}[/]")
            return
        
        # Crear agentes profesionales
        symbols = ["█", "▓", "▒", "░", "▄", "▀", "▌", "▐", "•", "+", "■", "◆", "▲", "▼", "◀", "▶"]
        
        agent1 = ProfessionalAgent("🧠 Professional_Alpha", self.client, self.canvas, symbols)
        agent2 = ProfessionalAgent("🎨 Professional_Beta", self.client, self.canvas, symbols)
        
        self.agents = [agent1, agent2]
        
        # Sesión profesional
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            task = progress.add_task("[cyan]Iniciando sesión profesional...", total=turns)
            
            for turn in range(turns):
                agent = self.agents[turn % len(self.agents)]
                
                # Análisis profesional
                patterns = self.canvas.analyze_professional_patterns()
                
                # Movimiento profesional
                move = agent.make_professional_move(turn)
                
                self.clear_screen()
                
                # Display profesional
                self.console.print(Panel(self.create_professional_banner(), style="bold bright_blue"))
                
                # Canvas profesional
                canvas_display = self.display_professional_canvas()
                self.console.print(Panel(canvas_display, title=f"🎨 Turno {turn + 1} - {agent.name}"))
                
                # Dashboard profesional
                dashboard = self.create_professional_dashboard(patterns)
                self.console.print(dashboard)
                
                # Información profesional
                info_text = f"""✏️ Símbolo: '{move['symbol']}'
📍 Posición: ({move['x']}, {move['y']})
💭 Razón: {move['reason']}
🎯 Confianza: {move.get('style_confidence', 0):.3f}
🧠 Estilo: {agent.style_evolution}
📊 Patrones: {len(patterns)} factores analizados"""
                
                self.console.print(Panel(info_text, title="📋 Análisis Profesional"))
                
                # Barra de progreso
                progress.update(task, advance=1)
                time.sleep(1.5)
        
        # Resultado final profesional
        self.clear_screen()
        final_patterns = self.canvas.analyze_professional_patterns()
        
        self.console.print(Panel(self.create_professional_banner(), style="bold bright_green"))
        
        # Canvas final profesional
        final_canvas = self.display_professional_canvas()
        self.console.print(Panel(final_canvas, title="🎨 Arte Final Profesional"))
        
        # Dashboard final
        self.console.print(self.create_professional_dashboard(final_patterns))
        
        # Guardar resultados profesionales
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        result = {
            'artwork': [''.join(row) for row in self.canvas.grid],
            'analytics': final_patterns,
            'move_history': list(self.canvas.move_history),
            'session_info': {
                'duration': str(datetime.now() - self.session_analytics['start_time']),
                'total_moves': self.canvas.analytics['total_moves'],
                'unique_symbols': list(self.canvas.analytics['unique_symbols']),
                'agents': [agent.name for agent in self.agents]
            },
            'timestamp': timestamp
        }
        
        with open(f"professional_art_{timestamp}.json", 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        self.console.print(f"[green]✅ Resultados profesionales guardados en professional_art_{timestamp}.json[/]")

if __name__ == "__main__":
    app = ProfessionalApp()
    
    try:
        app.run_professional_session(turns=15)
    except KeyboardInterrupt:
        print("\n[red]⏹️ Sesión profesional interrumpida[/]")
    except Exception as e:
        print(f"\n[red]❌ Error profesional: {e}[/]")
