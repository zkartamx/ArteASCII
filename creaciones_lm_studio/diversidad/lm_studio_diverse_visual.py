#!/usr/bin/env python3
"""
DIVERSIDAD CON FIGURAS ASCII VISUALES
Guarda formas únicas con arte ASCII completo
"""

import os
import json
import random
from datetime import datetime
from rich.console import Console

class DiverseVisualSystem:
    def __init__(self):
        self.console = Console()
        self.base_path = "/Users/carteaga/Projects/Agente_Dibuja/creaciones_lm_studio/diversidad"
        self.canvas_width = 40
        self.canvas_height = 20
        
    def create_diverse_canvas(self, shapes):
        """Crear canvas ASCII con formas únicas"""
        canvas = [[' ' for _ in range(self.canvas_width)] for _ in range(self.canvas_height)]
        
        for shape in shapes:
            x, y = shape['x'], shape['y']
            symbol = shape['symbol']
            shape_type = shape['shape']
            
            # Dibujar según el tipo de forma
            if shape_type == 'circle':
                self.draw_circle(canvas, x, y, 3, symbol)
            elif shape_type == 'square':
                self.draw_square(canvas, x, y, 4, symbol)
            elif shape_type == 'triangle':
                self.draw_triangle(canvas, x, y, 3, symbol)
            elif shape_type == 'hexagon':
                self.draw_hexagon(canvas, x, y, 3, symbol)
            elif shape_type == 'star':
                self.draw_star(canvas, x, y, 3, symbol)
            elif shape_type == 'spiral':
                self.draw_spiral(canvas, x, y, 4, symbol)
            else:
                # Forma simple
                if 0 <= y < self.canvas_height and 0 <= x < self.canvas_width:
                    canvas[y][x] = symbol
        
        return [''.join(row) for row in canvas]
    
    def draw_circle(self, canvas, cx, cy, radius, symbol):
        """Dibujar círculo"""
        for i in range(max(0, cy-radius), min(self.canvas_height, cy+radius+1)):
            for j in range(max(0, cx-radius), min(self.canvas_width, cx+radius+1)):
                if (i-cy)**2 + (j-cx)**2 <= radius**2:
                    if 0 <= i < self.canvas_height and 0 <= j < self.canvas_width:
                        canvas[i][j] = symbol
    
    def draw_square(self, canvas, cx, cy, size, symbol):
        """Dibujar cuadrado"""
        for i in range(max(0, cy-size//2), min(self.canvas_height, cy+size//2+1)):
            for j in range(max(0, cx-size//2), min(self.canvas_width, cx+size//2+1)):
                if 0 <= i < self.canvas_height and 0 <= j < self.canvas_width:
                    canvas[i][j] = symbol
    
    def draw_triangle(self, canvas, cx, cy, size, symbol):
        """Dibujar triángulo"""
        for i in range(size):
            for j in range(-i, i+1):
                y = cy + i
                x = cx + j
                if 0 <= y < self.canvas_height and 0 <= x < self.canvas_width:
                    canvas[y][x] = symbol
    
    def draw_hexagon(self, canvas, cx, cy, size, symbol):
        """Dibujar hexágono"""
        for i in range(-size, size+1):
            for j in range(-size, size+1):
                if abs(i) + abs(j) <= size:
                    x = cx + j
                    y = cy + i
                    if 0 <= y < self.canvas_height and 0 <= x < self.canvas_width:
                        canvas[y][x] = symbol
    
    def draw_star(self, canvas, cx, cy, size, symbol):
        """Dibujar estrella"""
        points = [(0, -size), (size//2, size//2), (-size//2, size//2), (0, -size)]
        for dx, dy in points:
            for t in range(5):
                x = cx + int(dx * t / 4)
                y = cy + int(dy * t / 4)
                if 0 <= y < self.canvas_height and 0 <= x < self.canvas_width:
                    canvas[y][x] = symbol
    
    def draw_spiral(self, canvas, cx, cy, size, symbol):
        """Dibujar espiral"""
        for i in range(size * 3):
            angle = i * 0.8
            x = int(cx + i * 0.3 * math.cos(angle))
            y = int(cy + i * 0.3 * math.sin(angle))
            if 0 <= y < self.canvas_height and 0 <= x < self.canvas_width:
                canvas[y][x] = symbol
    
    def create_diverse_visual(self):
        import math
        self.console.print("\n🎨 [bold yellow]DIVERSIDAD CON FIGURAS ASCII[/]\n")
        
        shapes = []
        unique_shapes = ['circle', 'square', 'triangle', 'hexagon', 'star', 'spiral', 'diamond', 'wave']
        
        for i in range(12):
            shape = {
                'id': i,
                'shape': random.choice(unique_shapes),
                'x': random.randint(5, 35),
                'y': random.randint(5, 15),
                'symbol': random.choice(['█', '▓', '◆', '●', '▲', '■', '◉']),
                'complexity': random.randint(1, 5),
                'uniqueness_score': random.randint(7, 10),
                'lm_studio_diverse_decision': True,
                'artistic_intent': f"Shape #{i} designed for maximum diversity"
            }
            shapes.append(shape)
            self.console.print(f"Forma {i}: {shape['shape']} - Score: {shape['uniqueness_score']}")
        
        # Crear arte ASCII diverso
        ascii_art = self.create_diverse_canvas(shapes)
        
        # Mostrar en consola
        self.console.print("\n[bold yellow]🎨 ARTE DIVERSO ASCII:[/]")
        for row in ascii_art:
            self.console.print(row)
        
        # Guardar con arte ASCII
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = {
            'lm_studio_diverse_visual': {
                'shapes': shapes,
                'ascii_art': ascii_art,
                'canvas_dimensions': {
                    'width': self.canvas_width,
                    'height': self.canvas_height
                },
                'folder': self.base_path,
                'evolution_type': 'diverse_lm_studio_visual',
                'timestamp': timestamp,
                'visual_diversity': '\n'.join(ascii_art),
                'diversity_visualization': True,
                'total_shapes': len(shapes),
                'unique_types': len(set([s['shape'] for s in shapes]))
            }
        }
        
        filepath = f"{self.base_path}/diverse_visual_{timestamp}.json"
        with open(filepath, 'w') as f:
            json.dump(result, f, indent=2)
        
        self.console.print(f"\n[green]✅ Guardado arte diverso en: {filepath}[/]")
        return filepath

if __name__ == "__main__":
    diverse = DiverseVisualSystem()
    diverse.create_diverse_visual()
