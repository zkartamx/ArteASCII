#!/usr/bin/env python3
"""
GENÉTICO CON FIGURAS ASCII VISUALES
Guarda creaciones con arte ASCII completo
"""

import os
import json
import random
from datetime import datetime
from rich.console import Console

class GeneticVisualSystem:
    def __init__(self):
        self.console = Console()
        self.base_path = "/Users/carteaga/Projects/Agente_Dibuja/creaciones_lm_studio/genetico"
        self.canvas_width = 40
        self.canvas_height = 20
        
    def create_ascii_canvas(self, population):
        """Crear canvas ASCII con las formas"""
        canvas = [[' ' for _ in range(self.canvas_width)] for _ in range(self.canvas_height)]
        
        for individual in population:
            x, y = individual['x'], individual['y']
            symbol = individual['symbol']
            shape = individual['shape']
            
            # Dibujar según la forma
            if shape == 'circle':
                self.draw_circle(canvas, x, y, individual['size'], symbol)
            elif shape == 'square':
                self.draw_square(canvas, x, y, individual['size'], symbol)
            elif shape == 'triangle':
                self.draw_triangle(canvas, x, y, individual['size'], symbol)
            elif shape == 'spiral':
                self.draw_spiral(canvas, x, y, individual['size'], symbol)
        
        return [''.join(row) for row in canvas]
    
    def draw_circle(self, canvas, cx, cy, size, symbol):
        """Dibujar círculo en canvas"""
        for i in range(max(0, cy-size), min(self.canvas_height, cy+size+1)):
            for j in range(max(0, cx-size), min(self.canvas_width, cx+size+1)):
                if (i-cy)**2 + (j-cx)**2 <= size**2:
                    if 0 <= i < self.canvas_height and 0 <= j < self.canvas_width:
                        canvas[i][j] = symbol
    
    def draw_square(self, canvas, cx, cy, size, symbol):
        """Dibujar cuadrado en canvas"""
        for i in range(max(0, cy-size//2), min(self.canvas_height, cy+size//2+1)):
            for j in range(max(0, cx-size//2), min(self.canvas_width, cx+size//2+1)):
                if 0 <= i < self.canvas_height and 0 <= j < self.canvas_width:
                    canvas[i][j] = symbol
    
    def draw_triangle(self, canvas, cx, cy, size, symbol):
        """Dibujar triángulo en canvas"""
        for i in range(size):
            for j in range(-i, i+1):
                y = cy + i
                x = cx + j
                if 0 <= y < self.canvas_height and 0 <= x < self.canvas_width:
                    canvas[y][x] = symbol
    
    def draw_spiral(self, canvas, cx, cy, size, symbol):
        """Dibujar espiral en canvas"""
        for i in range(size * 2):
            angle = i * 0.5
            x = int(cx + i * 0.5 * math.cos(angle))
            y = int(cy + i * 0.5 * math.sin(angle))
            if 0 <= y < self.canvas_height and 0 <= x < self.canvas_width:
                canvas[y][x] = symbol
    
    def create_genetic_evolution(self):
        import math
        self.console.print("\n🧬 [bold magenta]GENÉTICO CON FIGURAS ASCII[/]\n")
        
        population = []
        for i in range(6):
            individual = {
                'id': i,
                'shape': random.choice(['circle', 'square', 'triangle', 'spiral']),
                'x': random.randint(5, 35),
                'y': random.randint(5, 15),
                'size': random.randint(2, 4),
                'symbol': random.choice(['█', '▓', '◆', '●']),
                'fitness': random.randint(5, 10),
                'generation': random.randint(1, 3),
                'lm_studio_decision': True
            }
            population.append(individual)
            self.console.print(f"Individuo {i}: {individual['shape']} - Fitness: {individual['fitness']}")
        
        # Crear arte ASCII
        ascii_art = self.create_ascii_canvas(population)
        
        # Mostrar en consola
        self.console.print("\n[bold green]🎨 ARTE ASCII GENERADO:[/]")
        for row in ascii_art:
            self.console.print(row)
        
        # Guardar con arte ASCII
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = {
            'lm_studio_genetic_visual': {
                'population': population,
                'ascii_art': ascii_art,
                'canvas_dimensions': {
                    'width': self.canvas_width,
                    'height': self.canvas_height
                },
                'folder': self.base_path,
                'evolution_type': 'genetic_lm_studio_visual',
                'timestamp': timestamp,
                'visual_art': '\n'.join(ascii_art)
            }
        }
        
        filepath = f"{self.base_path}/genetic_visual_{timestamp}.json"
        with open(filepath, 'w') as f:
            json.dump(result, f, indent=2)
        
        self.console.print(f"\n[green]✅ Guardado arte ASCII en: {filepath}[/]")
        return filepath

if __name__ == "__main__":
    genetic = GeneticVisualSystem()
    genetic.create_genetic_evolution()
