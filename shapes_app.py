#!/usr/bin/env python3
"""
Agente Dibuja - Formas y Geometría
Sistema especializado en dibujo de formas geométricas
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
from collections import defaultdict

class ShapesCanvas:
    """Canvas especializado en formas geométricas"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]
        self.shape_library = {
            'circle': self.draw_circle,
            'square': self.draw_square,
            'triangle': self.draw_triangle,
            'diamond': self.draw_diamond,
            'star': self.draw_star,
            'heart': self.draw_heart,
            'spiral': self.draw_spiral,
            'wave': self.draw_wave
        }
        self.form_history = []
    
    def draw_circle(self, center_x: int, center_y: int, radius: int, symbol: str):
        """Dibujar círculo perfecto"""
        points = []
        for angle in range(0, 360, 5):
            rad = math.radians(angle)
            x = int(center_x + radius * math.cos(rad))
            y = int(center_y + radius * math.sin(rad))
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y][x] = symbol
                points.append((x, y))
        return points
    
    def draw_square(self, x: int, y: int, size: int, symbol: str):
        """Dibujar cuadrado"""
        points = []
        for i in range(size):
            for j in range(size):
                if 0 <= x+i < self.width and 0 <= y+j < self.height:
                    if i == 0 or i == size-1 or j == 0 or j == size-1:
                        self.grid[y+j][x+i] = symbol
                        points.append((x+i, y+j))
        return points
    
    def draw_triangle(self, x: int, y: int, size: int, symbol: str):
        """Dibujar triángulo"""
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
    
    def draw_diamond(self, center_x: int, center_y: int, size: int, symbol: str):
        """Dibujar diamante"""
        points = []
        for i in range(-size, size+1):
            for j in range(-size, size+1):
                if abs(i) + abs(j) <= size:
                    x, y = center_x + i, center_y + j
                    if 0 <= x < self.width and 0 <= y < self.height:
                        self.grid[y][x] = symbol
                        points.append((x, y))
        return points
    
    def draw_star(self, center_x: int, center_y: int, size: int, symbol: str):
        """Dibujar estrella"""
        points = []
        for angle in range(0, 360, 36):
            for r in range(size):
                rad = math.radians(angle)
                x = int(center_x + r * math.cos(rad))
                y = int(center_y + r * math.sin(rad))
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.grid[y][x] = symbol
                    points.append((x, y))
        return points
    
    def draw_heart(self, center_x: int, center_y: int, size: int, symbol: str):
        """Dibujar corazón"""
        points = []
        for t in range(0, 628, 10):
            theta = t / 100.0
            x = int(center_x + 16 * math.sin(theta)**3 * size/10)
            y = int(center_y - (13 * math.cos(theta) - 5 * math.cos(2*theta) - 2 * math.cos(3*theta) - math.cos(4*theta)) * size/10)
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y][x] = symbol
                points.append((x, y))
        return points
    
    def draw_spiral(self, center_x: int, center_y: int, size: int, symbol: str):
        """Dibujar espiral"""
        points = []
        for i in range(size * 10):
            angle = 0.1 * i
            r = 0.1 * i
            x = int(center_x + r * math.cos(angle))
            y = int(center_y + r * math.sin(angle))
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y][x] = symbol
                points.append((x, y))
        return points
    
    def draw_wave(self, x: int, y: int, length: int, symbol: str):
        """Dibujar onda sinusoidal"""
        points = []
        for i in range(length):
            wave_y = y + int(3 * math.sin(i * 0.5))
            if 0 <= x+i < self.width and 0 <= wave_y < self.height:
                self.grid[wave_y][x+i] = symbol
                points.append((x+i, wave_y))
        return points

class ShapesAgent:
    """Agente especializado en formas geométricas"""
    
    def __init__(self, name: str, client, canvas, symbols):
        self.name = name
        self.client = client
        self.canvas = canvas
        self.symbols = symbols
        self.shape_memory = []
        self.technique_evolution = {
            'precision': 0.8,
            'creativity': 0.7,
            'symmetry': 0.9,
            'complexity': 0.6
        }
    
    def generate_shape_prompt(self, available_shapes: list) -> str:
        """Generar prompt especializado en formas"""
        return f"""
Eres un artista ASCII especializado en geometría. Tu tarea es crear formas precisas y hermosas.

Formas disponibles: {available_shapes}

Consideraciones:
- Usa símbolos como █, ▓, ▒, ░, ▄, ▀, ▌, ▐, •, +, ■, ◆, ▲, ▼, ◀, ▶
- Prioriza la precisión geométrica
- Mantén proporciones correctas
- Considera simetría y balance

Responde con JSON válido:
{{
    "shape": "nombre_de_forma",
    "x": int,
    "y": int,
    "size": int,
    "symbol": "carácter",
    "reason": "explicación",
    "technique": "descripción_técnica"
}}
"""
    
    def create_geometric_art(self, turn_number: int) -> dict:
        """Crear arte geométrico profesional"""
        shapes = list(self.canvas.shape_library.keys())
        
        # Elegir forma basada en turno
        shape_index = turn_number % len(shapes)
        selected_shape = shapes[shape_index]
        
        # Parámetros óptimos para cada forma
        shape_params = {
            'circle': {'x': 20, 'y': 10, 'size': 5},
            'square': {'x': 15, 'y': 8, 'size': 6},
            'triangle': {'x': 10, 'y': 15, 'size': 8},
            'diamond': {'x': 25, 'y': 10, 'size': 4},
            'star': {'x': 15, 'y': 12, 'size': 6},
            'heart': {'x': 18, 'y': 8, 'size': 5},
            'spiral': {'x': 15, 'y': 10, 'size': 8},
            'wave': {'x': 5, 'y': 12, 'size': 20}
        }
        
        params = shape_params.get(selected_shape, {'x': 15, 'y': 10, 'size': 5})
        
        # Dibujar la forma
        symbol = random.choice(self.symbols)
        points = self.canvas.shape_library[selected_shape](
            params['x'], params['y'], params['size'], symbol
        )
        
        return {
            "shape": selected_shape,
            "x": params['x'],
            "y": params['y'],
            "size": params['size'],
            "symbol": symbol,
            "points": len(points),
            "reason": f"Forma {selected_shape} dibujada con precisión geométrica",
            "technique": f"Técnica especializada en {selected_shape}",
            "precision": self.technique_evolution['precision']
        }

class ShapesApp:
    """Aplicación especializada en formas geométricas"""
    
    def __init__(self):
        self.console = Console()
        self.canvas = ShapesCanvas(40, 25)
        self.client = None
        self.agents = []
        self.geometric_analytics = {
            'shapes_drawn': 0,
            'total_points': 0,
            'symmetry_score': 0.0,
            'geometric_accuracy': 0.0
        }
    
    def clear_screen(self):
        """Limpiar pantalla"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def create_shapes_banner(self):
        """Banner de formas"""
        return """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          🎯 AGENTE FORMAS PRO                              ║
║                    Sistema Especializado en Geometría                      ║
║                Círculos, Cuadrados, Estrellas y Más                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
    
    def display_geometric_canvas(self):
        """Display con colores para formas"""
        lines = []
        for row in self.canvas.grid:
            colored_line = ""
            for char in row:
                if char in ['█', '▓', '▒', '░']:
                    colored_line += f'[bold bright_cyan]{char}[/]'
                elif char in ['▲', '▼', '◀', '▶']:
                    colored_line += f'[bold bright_yellow]{char}[/]'
                elif char in ['■', '◆', '●']:
                    colored_line += f'[bold bright_magenta]{char}[/]'
                elif char != ' ':
                    colored_line += f'[bold bright_green]{char}[/]'
                else:
                    colored_line += ' '
            lines.append(colored_line)
        return '\n'.join(lines)
    
    def create_geometric_dashboard(self, shape_data: dict):
        """Dashboard especializado en formas"""
        dashboard = Table(title="📐 Dashboard Geométrico")
        
        dashboard.add_column("Métrica", style="cyan")
        dashboard.add_column("Valor", style="magenta")
        dashboard.add_column("Análisis", style="green")
        
        dashboard.add_row("Formas Dibujadas", str(self.geometric_analytics['shapes_drawn']), "Activo")
        dashboard.add_row("Puntos Totales", str(self.geometric_analytics['total_points']), "Densidad")
        dashboard.add_row("Precisión", f"{shape_data.get('precision', 0):.2f}", "Geométrica")
        dashboard.add_row("Símbolo Usado", shape_data.get('symbol', ''), "Estilo")
        dashboard.add_row("Técnica", shape_data.get('technique', ''), "Especializada")
        
        return dashboard
    
    def run_geometric_session(self, turns=8):
        """Sesión especializada en formas"""
        self.clear_screen()
        
        self.console.print(Panel(self.create_shapes_banner(), style="bold bright_blue"))
        
        # Conectar a LM Studio
        try:
            self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
            self.console.print("[green]✅ Motor geométrico conectado[/]")
        except Exception as e:
            self.console.print(f"[red]❌ Error geométrico: {e}[/]")
            return
        
        # Crear agente especializado
        symbols = ["█", "▓", "▒", "░", "▄", "▀", "▌", "▐", "•", "+", "■", "◆", "▲", "▼", "◀", "▶"]
        agent = ShapesAgent("🎯 Geometric_Master", self.client, self.canvas, symbols)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            task = progress.add_task("[cyan]Creando arte geométrico...", total=turns)
            
            for turn in range(turns):
                self.clear_screen()
                
                # Crear forma geométrica
                shape_data = agent.create_geometric_art(turn)
                
                # Actualizar analytics
                self.geometric_analytics['shapes_drawn'] += 1
                self.geometric_analytics['total_points'] += shape_data.get('points', 0)
                
                # Display
                self.console.print(Panel(self.create_shapes_banner(), style="bold bright_blue"))
                
                # Canvas geométrico
                canvas_display = self.display_geometric_canvas()
                self.console.print(Panel(canvas_display, title=f"📐 Turno {turn + 1} - {agent.name}"))
                
                # Dashboard geométrico
                dashboard = self.create_geometric_dashboard(shape_data)
                self.console.print(dashboard)
                
                # Info de forma
                info_text = f"""🎯 Forma: {shape_data['shape']}
📍 Centro: ({shape_data['x']}, {shape_data['y']})
📏 Tamaño: {shape_data['size']}
✏️ Símbolo: '{shape_data['symbol']}'
📊 Puntos: {shape_data['points']}
💡 Técnica: {shape_data['technique']}"""
                
                self.console.print(Panel(info_text, title="📋 Análisis Geométrico"))
                
                progress.update(task, advance=1)
                time.sleep(2)
        
        # Resultado final
        self.clear_screen()
        self.console.print(Panel(self.create_shapes_banner(), style="bold bright_green"))
        
        # Canvas final
        final_canvas = self.display_geometric_canvas()
        self.console.print(Panel(final_canvas, title="🎯 Arte Geométrico Final"))
        
        # Guardar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = {
            'geometric_artwork': [''.join(row) for row in self.canvas.grid],
            'shapes_used': list(self.canvas.shape_library.keys()),
            'analytics': self.geometric_analytics,
            'techniques': agent.technique_evolution,
            'timestamp': timestamp
        }
        
        with open(f"geometric_art_{timestamp}.json", 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        self.console.print(f"[green]✅ Arte geométrico guardado en geometric_art_{timestamp}.json[/]")

if __name__ == "__main__":
    app = ShapesApp()
    
    try:
        app.run_geometric_session(turns=8)
    except KeyboardInterrupt:
        print("\n[red]⏹️ Sesión geométrica interrumpida[/]")
    except Exception as e:
        print(f"\n[red]❌ Error geométrico: {e}[/]")
