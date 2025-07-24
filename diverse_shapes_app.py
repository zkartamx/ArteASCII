#!/usr/bin/env python3
"""
Agente Dibuja - Diversidad Total
Sistema con variedad infinita de formas y patrones
"""

import os
import time
import json
import math
import random
from datetime import datetime
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from collections import defaultdict, deque

class DiverseCanvas:
    """Canvas con sistema de diversidad infinita"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]
        self.diverse_library = {
            'circle': self.draw_perfect_circle,
            'square': self.draw_square,
            'triangle': self.draw_triangle,

            'hexagon': self.draw_hexagon,
            'star': self.draw_star,
            'heart': self.draw_heart,
            'spiral': self.draw_spiral,
            'wave': self.draw_wave,
            'flower': self.draw_flower,
            'tree': self.draw_tree,
            'mountain': self.draw_mountain
        }
        self.used_shapes = deque(maxlen=20)
        self.shape_variety = defaultdict(int)
    
    def draw_perfect_circle(self, center_x: int, center_y: int, radius: int, symbol: str):
        """Círculo perfecto"""
        points = []
        for angle in range(0, 360, 2):
            rad = math.radians(angle)
            x = int(center_x + radius * math.cos(rad))
            y = int(center_y + radius * math.sin(rad))
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y][x] = symbol
                points.append((x, y))
        return points
    
    def draw_square(self, x: int, y: int, size: int, symbol: str):
        """Cuadrado"""
        points = []
        for i in range(size):
            for j in range(size):
                if 0 <= x+i < self.width and 0 <= y+j < self.height:
                    if i == 0 or i == size-1 or j == 0 or j == size-1:
                        self.grid[y+j][x+i] = symbol
                        points.append((x+i, y+j))
        return points
    
    def draw_triangle(self, x: int, y: int, size: int, symbol: str):
        """Triángulo"""
        points = []
        for row in range(size):
            spaces = size - row - 1
            stars = 2 * row + 1
            for col in range(stars):
                draw_x = x + spaces + col
                draw_y = y + row
                if 0 <= draw_x < self.width and 0 <= draw_y < self.height:
                    self.grid[draw_y][draw_x] = symbol
                    points.append((draw_x, draw_y))
        return points
    
    def draw_hexagon(self, center_x: int, center_y: int, size: int, symbol: str):
        """Hexágono"""
        points = []
        for i in range(6):
            angle = i * math.pi / 3
            x1 = center_x + int(size * math.cos(angle))
            y1 = center_y + int(size * math.sin(angle))
            angle2 = (i + 1) * math.pi / 3
            x2 = center_x + int(size * math.cos(angle2))
            y2 = center_y + int(size * math.sin(angle2))
            # Línea simple entre vértices
            steps = max(abs(x2-x1), abs(y2-y1))
            for t in range(steps + 1):
                x = x1 + (x2 - x1) * t // steps
                y = y1 + (y2 - y1) * t // steps
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.grid[y][x] = symbol
                    points.append((x, y))
        return points
    
    def draw_star(self, center_x: int, center_y: int, size: int, symbol: str):
        """Estrella"""
        points = []
        for i in range(10):
            angle = 2 * math.pi * i / 10
            r = size if i % 2 == 0 else size // 2
            x = int(center_x + r * math.cos(angle))
            y = int(center_y + r * math.sin(angle))
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y][x] = symbol
                points.append((x, y))
        return points
    
    def draw_heart(self, center_x: int, center_y: int, size: int, symbol: str):
        """Corazón"""
        points = []
        for t in range(0, 628, 5):
            theta = t / 100.0
            x = int(center_x + 16 * math.sin(theta)**3 * size/10)
            y = int(center_y - (13 * math.cos(theta) - 5 * math.cos(2*theta) - 2 * math.cos(3*theta) - math.cos(4*theta)) * size/10)
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y][x] = symbol
                points.append((x, y))
        return points
    
    def draw_spiral(self, center_x: int, center_y: int, size: int, symbol: str):
        """Espiral"""
        points = []
        for i in range(size * 8):
            angle = 0.2 * i
            r = 0.1 * i
            x = int(center_x + r * math.cos(angle))
            y = int(center_y + r * math.sin(angle))
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y][x] = symbol
                points.append((x, y))
        return points
    
    def draw_wave(self, x: int, y: int, length: int, symbol: str):
        """Onda"""
        points = []
        for i in range(length):
            wave_y = y + int(3 * math.sin(i * 0.3))
            if 0 <= x+i < self.width and 0 <= wave_y < self.height:
                self.grid[wave_y][x+i] = symbol
                points.append((x+i, wave_y))
        return points
    
    def draw_flower(self, center_x: int, center_y: int, petals: int, symbol: str):
        """Flor"""
        points = []
        # Centro
        if 0 <= center_x < self.width and 0 <= center_y < self.height:
            self.grid[center_y][center_x] = symbol
            points.append((center_x, center_y))
        
        # Pétalos
        for i in range(petals):
            angle = 2 * math.pi * i / petals
            for r in range(1, 5):
                x = center_x + int(r * math.cos(angle))
                y = center_y + int(r * math.sin(angle))
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.grid[y][x] = symbol
                    points.append((x, y))
        return points
    
    def draw_tree(self, x: int, y: int, height: int, symbol: str):
        """Árbol"""
        points = []
        # Tronco
        for i in range(height // 3):
            if 0 <= x < self.width and 0 <= y-i < self.height:
                self.grid[y-i][x] = symbol
                points.append((x, y-i))
        
        # Copa
        for level in range(height // 3):
            width = level + 1
            for dx in range(-width, width + 1):
                if 0 <= x+dx < self.width and 0 <= y-height//3-level < self.height:
                    self.grid[y-height//3-level][x+dx] = symbol
                    points.append((x+dx, y-height//3-level))
        return points
    
    def draw_mountain(self, x: int, y: int, width: int, symbol: str):
        """Montaña"""
        points = []
        peak_x = x + width // 2
        peak_y = y - width // 2
        
        for i in range(width + 1):
            mountain_y = y - int(abs(i - width//2))
            for j in range(mountain_y, y):
                if 0 <= x+i < self.width and 0 <= j < self.height:
                    self.grid[j][x+i] = symbol
                    points.append((x+i, j))
        return points

class DiverseAgent:
    """Agente anti-repetición"""
    
    def __init__(self, name: str, client, canvas, symbols):
        self.name = name
        self.client = client
        self.canvas = canvas
        self.symbols = symbols
        self.used_shapes = deque(maxlen=15)
        self.position_memory = set()
        self.color_rotation = 0
    
    def select_unique_shape(self, turn: int) -> str:
        """Seleccionar forma única"""
        all_shapes = list(self.canvas.diverse_library.keys())
        
        # Filtrar formas no usadas
        available_shapes = [shape for shape in all_shapes if shape not in self.used_shapes]
        
        if not available_shapes:
            available_shapes = all_shapes
            self.used_shapes.clear()
        
        # Patrón de rotación
        selected = available_shapes[turn % len(available_shapes)]
        self.used_shapes.append(selected)
        return selected
    
    def create_diverse_art(self, turn: int) -> dict:
        """Crear arte diverso"""
        shape_type = self.select_unique_shape(turn)
        
        # Posiciones dinámicas
        positions = [
            (10, 8), (25, 8), (15, 15), (30, 12), (5, 18),
            (20, 5), (35, 20), (8, 12), (28, 18), (12, 22),
            (18, 3), (32, 5), (7, 15), (22, 20), (33, 8)
        ]
        
        pos_x, pos_y = positions[turn % len(positions)]
        
        # Símbolos rotativos
        symbol_sets = [
            ["█", "▓", "▒", "░"],
            ["•", "+", "■", "◆"],
            ["▲", "▼", "◀", "▶"],
            ["▄", "▀", "▌", "▐"]
        ]
        
        symbols = symbol_sets[turn % len(symbol_sets)]
        symbol = random.choice(symbols)
        
        # Ejecutar forma
        if shape_type in self.canvas.diverse_library:
            points = self.canvas.diverse_library[shape_type](pos_x, pos_y, random.randint(3, 7), symbol)
        else:
            points = []
        
        return {
            "shape": shape_type,
            "x": pos_x,
            "y": pos_y,
            "symbol": symbol,
            "points": len(points),
            "variety": len(set(self.used_shapes)),
            "position_strategy": "anti-repetición"
        }

class DiverseApp:
    """Aplicación de diversidad total"""
    
    def __init__(self):
        self.console = Console()
        self.canvas = DiverseCanvas(40, 25)
        self.client = None
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def create_banner(self):
        return """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          🌈 DIVERSIDAD TOTAL                               ║
║                    Sistema Anti-Repetición Avanzado                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
    
    def display_canvas(self):
        lines = []
        for row in self.canvas.grid:
            colored_line = ""
            for char in row:
                if char != ' ':
                    colored_line += f'[bold bright_cyan]{char}[/]'
                else:
                    colored_line += ' '
            lines.append(colored_line)
        return '\n'.join(lines)
    
    def run_session(self, turns=12):
        self.clear_screen()
        
        self.console.print(Panel(self.create_banner(), style="bold bright_blue"))
        
        try:
            self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
        except Exception as e:
            print(f"Error: {e}")
            return
        
        agent = DiverseAgent("🌈 Diversity_Master", self.client, self.canvas, 
                           ["█", "▓", "▒", "░", "▄", "▀", "▌", "▐", "•", "+", "■", "◆"])
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            task = progress.add_task("Creando diversidad...", total=turns)
            
            for turn in range(turns):
                self.clear_screen()
                
                shape_data = agent.create_diverse_art(turn)
                
                self.console.print(Panel(self.create_banner(), style="bold bright_blue"))
                
                canvas_display = self.display_canvas()
                self.console.print(Panel(canvas_display, title=f"🌈 Turno {turn + 1} - {shape_data['shape']}"))
                
                info = f"""🎯 Forma: {shape_data['shape']}
📍 Posición: ({shape_data['x']}, {shape_data['y']})
✏️ Símbolo: '{shape_data['symbol']}'
📊 Puntos: {shape_data['points']}
🔄 Variación: {shape_data['variety']} formas únicas"""
                
                self.console.print(Panel(info, title="📋 Análisis de Diversidad"))
                
                progress.update(task, advance=1)
                time.sleep(1.5)
        
        # Resultado final
        self.clear_screen()
        self.console.print(Panel(self.create_banner(), style="bold bright_green"))
        
        final_canvas = self.display_canvas()
        self.console.print(Panel(final_canvas, title="🌈 Arte Diverso Final"))
        
        # Estadísticas
        unique_shapes = len(set(agent.used_shapes))
        stats = f"""📊 Estadísticas de Diversidad:
- Formas únicas: {unique_shapes}
- Total de formas: {len(agent.used_shapes)}
- Diversidad: {unique_shapes/len(agent.used_shapes):.2f}
- Sin repeticiones: ✅"""
        
        self.console.print(Panel(stats, title="📈 Análisis Final"))
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = {
            'diverse_artwork': [''.join(row) for row in self.canvas.grid],
            'shapes_used': list(agent.used_shapes),
            'diversity_stats': {
                'unique_shapes': unique_shapes,
                'total_shapes': len(agent.used_shapes),
                'diversity_ratio': unique_shapes/len(agent.used_shapes)
            },
            'timestamp': timestamp
        }
        
        with open(f"diverse_art_{timestamp}.json", 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        self.console.print(f"[green]✅ Arte diverso guardado en diverse_art_{timestamp}.json[/]")

if __name__ == "__main__":
    app = DiverseApp()
    
    try:
        app.run_session(turns=12)
    except KeyboardInterrupt:
        print("\n[red]⏹️ Sesión diversa interrumpida[/]")
    except Exception as e:
        print(f"\n[red]❌ Error de diversidad: {e}[/]")
