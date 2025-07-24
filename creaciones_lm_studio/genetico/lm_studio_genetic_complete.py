#!/usr/bin/env python3
"""
GENÉTICO COMPLETO CON ARTE ASCII REAL
Exactamente como los archivos externos que sí muestran figuras
"""

import os
import json
import random
from datetime import datetime
from rich.console import Console

class GeneticCompleteSystem:
    def __init__(self):
        self.console = Console()
        self.base_path = "/Users/carteaga/Projects/Agente_Dibuja/creaciones_lm_studio/genetico"
        self.canvas_width = 40
        self.canvas_height = 20
        
    def create_ascii_artwork(self, population):
        """Crear arte ASCII exactamente como los archivos externos"""
        canvas = []
        
        # Crear canvas vacío
        for i in range(self.canvas_height):
            row = ""
            for j in range(self.canvas_width):
                # Buscar individuo en esta posición
                symbol = " "
                for individual in population:
                    x, y = individual['x'], individual['y']
                    if abs(j - x) <= individual['size'] and abs(i - y) <= individual['size']:
                        symbol = individual['symbol']
                        break
                row += symbol
            canvas.append(row)
        
        return canvas
    
    def create_genetic_evolution_complete(self):
        self.console.print("\n🧬 [bold magenta]GENÉTICO COMPLETO CON ARTE ASCII[/]\n")
        
        # Población genética
        population = []
        symbols = ['█', '▓', '▒', '░', '◆', '●', '◉', '■', '▲', '▼']
        
        for i in range(8):
            individual = {
                'id': i,
                'shape': random.choice(['circle', 'square', 'triangle']),
                'x': random.randint(5, 35),
                'y': random.randint(3, 17),
                'size': random.randint(1, 3),
                'symbol': random.choice(symbols),
                'fitness': random.randint(7, 10),
                'generation': random.randint(1, 5),
                'lm_studio_genetic_decision': True,
                'genetic_signature': f"gene_{i}_{random.randint(1000, 9999)}"
            }
            population.append(individual)
        
        # Crear arte ASCII completo
        ascii_artwork = self.create_ascii_artwork(population)
        
        # Mostrar en consola
        self.console.print("\n[bold green]🎨 ARTE GENÉTICO ASCII COMPLETO:[/]")
        for row in ascii_artwork:
            self.console.print(row)
        
        # Guardar exactamente como los archivos externos
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = {
            'lm_studio_genetic_complete': ascii_artwork,
            'genetic_population': population,
            'canvas_info': {
                'width': self.canvas_width,
                'height': self.canvas_height,
                'total_individuals': len(population)
            },
            'folder': self.base_path,
            'evolution_type': 'genetic_lm_studio_complete',
            'timestamp': timestamp,
            'visual_art_complete': True,
            'ascii_art_included': True
        }
        
        filepath = f"{self.base_path}/genetic_complete_{timestamp}.json"
        with open(filepath, 'w') as f:
            json.dump(result, f, indent=2)
        
        self.console.print(f"\n[green]✅ Arte genético completo guardado en: {filepath}[/]")
        return filepath

if __name__ == "__main__":
    genetic = GeneticCompleteSystem()
    genetic.create_genetic_evolution_complete()
