#!/usr/bin/env python3
"""
Agente Dibuja - Evolución Cuántica
Sistema de arte ASCII con fractales cuánticos y evolución avanzada
"""

import os
import time
import json
import math
import random
import cmath
from datetime import datetime
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from collections import defaultdict, deque

class QuantumFractal:
    """Fractales cuánticos complejos"""
    
    def __init__(self):
        self.quantum_states = ['superposition', 'entanglement', 'coherence', 'decoherence']
        self.complexity_level = random.uniform(2, 8)
        self.quantum_noise = random.uniform(0.1, 0.5)
    
    def mandelbrot_quantum(self, center_x, center_y, size, symbol):
        """Conjunto de Mandelbrot cuántico"""
        points = []
        
        for px in range(-size, size + 1):
            for py in range(-size, size + 1):
                # Mapeo a plano complejo
                x0 = (center_x + px - 2.5) / (size / 3.5)
                y0 = (center_y + py - 2.5) / (size / 2)
                
                x, y = 0.0, 0.0
                iteration = 0
                max_iteration = 100
                
                while x*x + y*y <= 4 and iteration < max_iteration:
                    xtemp = x*x - y*y + x0
                    y = 2*x*y + y0
                    x = xtemp
                    iteration += 1
                
                if iteration < max_iteration:
                    if 0 <= center_x + px < 40 and 0 <= center_y + py < 25:
                        # Efecto cuántico: probabilidad de punto
                        quantum_probability = iteration / max_iteration
                        if random.random() < quantum_probability:
                            points.append((center_x + px, center_y + py))
        
        return points
    
    def julia_quantum(self, center_x, center_y, size, symbol, c_real=-0.7, c_imag=0.27015):
        """Conjunto de Julia cuántico"""
        points = []
        c = complex(c_real, c_imag)
        
        for px in range(-size, size + 1):
            for py in range(-size, size + 1):
                z = complex((center_x + px - 2.5) / (size / 3), 
                           (center_y + py - 2.5) / (size / 2))
                
                iteration = 0
                max_iteration = 50
                
                while abs(z) <= 2 and iteration < max_iteration:
                    z = z*z + c
                    iteration += 1
                
                if iteration < max_iteration:
                    if 0 <= center_x + px < 40 and 0 <= center_y + py < 25:
                        # Efecto cuántico: superposición de estados
                        quantum_state = iteration % 4
                        if quantum_state == 0:
                            points.append((center_x + px, center_y + py))
        
        return points
    
    def sierpinski_quantum(self, x, y, size, symbol):
        """Triángulo de Sierpinski cuántico"""
        points = []
        
        def quantum_triangle(ax, ay, bx, by, cx, cy, depth):
            if depth == 0:
                return
            
            # Efecto cuántico: probabilidad de subdivisión
            if random.random() < 0.8:  # 80% de probabilidad de subdivisión
                # Puntos medios con variación cuántica
                dx = random.uniform(-0.5, 0.5)
                dy = random.uniform(-0.5, 0.5)
                
                ab_x = (ax + bx) // 2 + int(dx * 2)
                ab_y = (ay + by) // 2 + int(dy * 2)
                bc_x = (bx + cx) // 2 + int(dx * 2)
                bc_y = (by + cy) // 2 + int(dy * 2)
                ca_x = (cx + ax) // 2 + int(dx * 2)
                ca_y = (cy + ay) // 2 + int(dy * 2)
                
                # Dibujar triángulo cuántico
                for px, py in [(ax, ay), (bx, by), (cx, cy)]:
                    if 0 <= px < 40 and 0 <= py < 25:
                        points.append((px, py))
                
                # Recursión cuántica
                quantum_triangle(ax, ay, ab_x, ab_y, ca_x, ca_y, depth - 1)
                quantum_triangle(ab_x, ab_y, bx, by, bc_x, bc_y, depth - 1)
                quantum_triangle(ca_x, ca_y, bc_x, bc_y, cx, cy, depth - 1)
        
        quantum_triangle(x, y, x + size, y, x + size//2, y - size, 4)
        return points
    
    def koch_quantum(self, x, y, size, symbol):
        """Copo de nieve de Koch cuántico"""
        points = []
        
        def quantum_koch_line(x1, y1, x2, y2, depth):
            if depth == 0:
                # Dibujar línea cuántica
                steps = max(abs(x2-x1), abs(y2-y1))
                for t in range(steps + 1):
                    px = x1 + (x2 - x1) * t // max(steps, 1)
                    py = y1 + (y2 - y1) * t // max(steps, 1)
                    if 0 <= px < 40 and 0 <= py < 25:
                        # Efecto cuántico: probabilidad de punto
                        if random.random() < 0.9:
                            points.append((px, py))
                return
            
            # División cuántica de Koch
            dx = x2 - x1
            dy = y2 - y1
            
            # Puntos de Koch con variación cuántica
            x1_new = x1
            y1_new = y1
            x2_new = x1 + dx // 3 + random.randint(-1, 1)
            y2_new = y1 + dy // 3 + random.randint(-1, 1)
            x3_new = x1 + dx // 2 - dy // 3 + random.randint(-1, 1)
            y3_new = y1 + dy // 2 + dx // 3 + random.randint(-1, 1)
            x4_new = x1 + 2 * dx // 3 + random.randint(-1, 1)
            y4_new = y1 + 2 * dy // 3 + random.randint(-1, 1)
            x5_new = x2
            y5_new = y2
            
            quantum_koch_line(x1_new, y1_new, x2_new, y2_new, depth - 1)
            quantum_koch_line(x2_new, y2_new, x3_new, y3_new, depth - 1)
            quantum_koch_line(x3_new, y3_new, x4_new, y4_new, depth - 1)
            quantum_koch_line(x4_new, y4_new, x5_new, y5_new, depth - 1)
        
        # Crear copo de noche cuántico
        quantum_koch_line(x, y, x + size, y, 3)
        quantum_koch_line(x + size, y, x + size//2, y - size, 3)
        quantum_koch_line(x + size//2, y - size, x, y, 3)
        
        return points

class QuantumCanvas:
    """Canvas cuántico con fractales"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]
        self.quantum_fractals = QuantumFractal()
        self.quantum_states = []
        self.coherence_level = 1.0
        
    def draw_quantum_shape(self, shape_type: str, x: int, y: int, size: int, symbol: str):
        """Dibujar forma cuántica"""
        points = []
        
        if shape_type == 'mandelbrot':
            points = self.quantum_fractals.mandelbrot_quantum(x, y, size, symbol)
        elif shape_type == 'julia':
            points = self.quantum_fractals.julia_quantum(x, y, size, symbol)
        elif shape_type == 'sierpinski':
            points = self.quantum_fractals.sierpinski_quantum(x, y, size, symbol)
        elif shape_type == 'koch':
            points = self.quantum_fractals.koch_quantum(x, y, size, symbol)
        elif shape_type == 'quantum_spiral':
            points = self.draw_quantum_spiral(x, y, size, symbol)
        elif shape_type == 'quantum_wave':
            points = self.draw_quantum_wave(x, y, size, symbol)
        
        # Aplicar puntos con decoherencia cuántica
        for px, py in points:
            if 0 <= px < self.width and 0 <= py < self.height:
                # Efecto cuántico: probabilidad de aparición
                if random.random() < self.coherence_level:
                    self.grid[py][px] = symbol
        
        return points
    
    def draw_quantum_spiral(self, center_x, center_y, size, symbol):
        """Espiral cuántica con decoherencia"""
        points = []
        
        for i in range(size * 20):
            # Ángulo cuántico con incertidumbre
            angle = 0.1 * i + random.uniform(-0.1, 0.1)
            radius = 0.05 * i * (1 + random.uniform(-0.1, 0.1))
            
            x = int(center_x + radius * math.cos(angle))
            y = int(center_y + radius * math.sin(angle))
            
            if 0 <= x < self.width and 0 <= y < self.height:
                # Probabilidad cuántica de aparición
                probability = 1 - (i / (size * 20))
                if random.random() < probability:
                    points.append((x, y))
        
        return points
    
    def draw_quantum_wave(self, x, y, length, symbol):
        """Onda cuántica con superposición"""
        points = []
        
        for i in range(length):
            # Onda con múltiples estados superpuestos
            wave_y = y + int(3 * math.sin(i * 0.3))
            wave_y2 = y + int(2 * math.sin(i * 0.5))  # Segunda onda superpuesta
            wave_y3 = y + int(1 * math.sin(i * 0.7))  # Tercera onda superpuesta
            
            # Probabilidad de colapso a cada estado
            states = [wave_y, wave_y2, wave_y3]
            collapsed_state = random.choice(states)
            
            if 0 <= x+i < self.width and 0 <= collapsed_state < self.height:
                points.append((x+i, collapsed_state))
        
        return points

class QuantumArtist:
    """Agente cuántico con decoherencia controlada"""
    
    def __init__(self, name: str, client, canvas):
        self.name = name
        self.client = client
        self.canvas = canvas
        self.quantum_states = ['coherent', 'decoherent', 'superposed', 'collapsed']
        self.coherence_history = []
        
    def create_quantum_art(self, iteration: int) -> dict:
        """Crear arte cuántico con decoherencia"""
        
        # Estados cuánticos disponibles
        quantum_shapes = [
            'mandelbrot', 'julia', 'sierpinski', 'koch', 
            'quantum_spiral', 'quantum_wave'
        ]
        
        # Posiciones cuánticas (superposición)
        quantum_positions = [
            (10, 8), (25, 8), (15, 15), (30, 12), (5, 18),
            (20, 5), (35, 20), (8, 12), (28, 18), (12, 22),
            (18, 3), (32, 5), (7, 15), (22, 20), (33, 8)
        ]
        
        # Símbolos cuánticos con decoherencia
        quantum_symbols = ["█", "▓", "▒", "░", "▌", "▐", "◆", "●", "■", "◉"]
        
        # Selección cuántica
        shape_type = quantum_shapes[iteration % len(quantum_shapes)]
        pos_x, pos_y = quantum_positions[iteration % len(quantum_positions)]
        symbol = quantum_symbols[iteration % len(quantum_symbols)]
        
        # Coherencia cuántica variable
        self.canvas.coherence_level = 0.7 + 0.3 * math.sin(iteration * 0.5)
        
        # Dibujar forma cuántica
        points = self.canvas.draw_quantum_shape(shape_type, pos_x, pos_y, 
                                              random.randint(4, 8), symbol)
        
        # Estado cuántico actual
        current_state = self.quantum_states[iteration % len(self.quantum_states)]
        self.coherence_history.append(self.canvas.coherence_level)
        
        return {
            "iteration": iteration,
            "quantum_shape": shape_type,
            "quantum_position": (pos_x, pos_y),
            "quantum_symbol": symbol,
            "coherence_level": self.canvas.coherence_level,
            "quantum_state": current_state,
            "quantum_points": len(points),
            "decoherence_factor": 1 - self.canvas.coherence_level
        }

class QuantumEvolutionApp:
    """Aplicación de evolución cuántica"""
    
    def __init__(self):
        self.console = Console()
        self.canvas = QuantumCanvas(40, 25)
        self.client = None
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def create_banner(self):
        return """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          ⚛️ EVOLUCIÓN CUÁNTICA                             ║
║                    Fractales Cuánticos y Decoherencia                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
    
    def display_canvas(self):
        lines = []
        for row in self.canvas.grid:
            colored_line = ""
            for char in row:
                if char != ' ':
                    # Colores cuánticos basados en decoherencia
                    decoherence_factor = 1 - self.canvas.coherence_level
                    if decoherence_factor < 0.3:
                        colored_line += f'[bold bright_cyan]{char}[/]'
                    elif decoherence_factor < 0.6:
                        colored_line += f'[bold bright_magenta]{char}[/]'
                    else:
                        colored_line += f'[bold bright_yellow]{char}[/]'
                else:
                    colored_line += ' '
            lines.append(colored_line)
        return '\n'.join(lines)
    
    def display_quantum_stats(self, quantum_data):
        """Mostrar estadísticas cuánticas"""
        table = Table(title="⚛️ Estadísticas Cuánticas")
        table.add_column("Métrica Cuántica", style="cyan")
        table.add_column("Valor", style="magenta")
        
        table.add_row("Iteración", str(quantum_data['iteration']))
        table.add_row("Forma Cuántica", quantum_data['quantum_shape'])
        table.add_row("Estado Cuántico", quantum_data['quantum_state'])
        table.add_row("Coherencia", f"{quantum_data['coherence_level']:.3f}")
        table.add_row("Decoherencia", f"{quantum_data['decoherence_factor']:.3f}")
        table.add_row("Puntos Cuánticos", str(quantum_data['quantum_points']))
        
        return table
    
    def run_quantum_evolution(self, iterations=15):
        self.clear_screen()
        
        self.console.print(Panel(self.create_banner(), style="bold bright_cyan"))
        
        try:
            self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
        except Exception as e:
            print(f"Error: {e}")
            return
        
        quantum_artist = QuantumArtist("⚛️ Quantum_Master", self.client, self.canvas)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            task = progress.add_task("Colapsando funciones de onda...", total=iterations)
            
            for iteration in range(iterations):
                self.clear_screen()
                
                quantum_data = quantum_artist.create_quantum_art(iteration)
                
                self.console.print(Panel(self.create_banner(), style="bold bright_cyan"))
                
                canvas_display = self.display_canvas()
                self.console.print(Panel(canvas_display, title=f"⚛️ Iteración {iteration + 1}"))
                
                stats_table = self.display_quantum_stats(quantum_data)
                self.console.print(stats_table)
                
                # Información cuántica
                quantum_info = f"""🔬 Información Cuántica:
- Forma: {quantum_data['quantum_shape']}
- Posición: {quantum_data['quantum_position']}
- Símbolo: {quantum_data['quantum_symbol']}
- Estado: {quantum_data['quantum_state']}
- Coherencia: {quantum_data['coherence_level']:.3f}
- Decoherencia: {quantum_data['decoherence_factor']:.3f}"""
                
                self.console.print(Panel(quantum_info, title="⚛️ Análisis Cuántico"))
                
                progress.update(task, advance=1)
                time.sleep(1.5)
        
        # Resultado final cuántico
        self.clear_screen()
        self.console.print(Panel(self.create_banner(), style="bold bright_green"))
        
        final_canvas = self.display_canvas()
        self.console.print(Panel(final_canvas, title="⚛️ Arte Cuántico Final"))
        
        # Estadísticas cuánticas finales
        quantum_stats = f"""⚛️ Evolución Cuántica Completada:
- Iteraciones: {iterations}
- Estados cuánticos: {len(set(['mandelbrot', 'julia', 'sierpinski', 'koch', 'quantum_spiral', 'quantum_wave']))}
- Coherencia promedio: {sum(quantum_artist.coherence_history)/len(quantum_artist.coherence_history):.3f}
- Decoherencia total: {1 - (sum(quantum_artist.coherence_history)/len(quantum_artist.coherence_history)):.3f}
- Formas fractales: 6 tipos
- Estados superpuestos: ✅
- Colapso cuántico: ✅"""
        
        self.console.print(Panel(quantum_stats, title="📊 Análisis Cuántico Final"))
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = {
            'quantum_artwork': [''.join(row) for row in self.canvas.grid],
            'quantum_iterations': iterations,
            'quantum_shapes': ['mandelbrot', 'julia', 'sierpinski', 'koch', 'quantum_spiral', 'quantum_wave'],
            'coherence_history': quantum_artist.coherence_history,
            'quantum_states': ['coherent', 'decoherent', 'superposed', 'collapsed'],
            'timestamp': timestamp
        }
        
        with open(f"quantum_evolution_{timestamp}.json", 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        self.console.print(f"[green]✅ Evolución cuántica guardada en quantum_evolution_{timestamp}.json[/]")

if __name__ == "__main__":
    app = QuantumEvolutionApp()
    
    try:
        app.run_quantum_evolution(iterations=15)
    except KeyboardInterrupt:
        print("\n[red]⏹️ Evolución cuántica interrumpida[/]")
    except Exception as e:
        print(f"\n[red]❌ Error cuántico: {e}[/]")
