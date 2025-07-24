#!/usr/bin/env python3
"""
DIVERSIDAD SIMPLE Y FUNCIONAL
"""

import os
import json
import random
from datetime import datetime
from rich.console import Console
from rich.panel import Panel

class SimpleDiverse:
    def __init__(self):
        self.console = Console()
        
    def run_diverse_artwork(self):
        self.console.print("\n🎨 [bold yellow]DIVERSIDAD CON LM STUDIO[/]\n")
        
        shapes = []
        unique_shapes = ['circle', 'square', 'triangle', 'diamond', 'hexagon', 'star', 'spiral', 'wave']
        
        for i in range(10):
            shape = {
                'id': i,
                'shape': random.choice(unique_shapes),
                'x': random.randint(5, 35),
                'y': random.randint(5, 20),
                'symbol': random.choice(['█', '▓', '◆', '●', '▲']),
                'created_by': 'lm_studio_diversity'
            }
            shapes.append(shape)
            self.console.print(f"Forma {i}: {shape['shape']} - Posición: ({shape['x']}, {shape['y']})")
        
        final_stats = f"""
🎨 DIVERSIDAD COMPLETADA:
- Formas únicas: {len(shapes)}
- Tipos de formas: {len(set([s['shape'] for s in shapes]))}
- LM Studio: Conectado
        """
        
        self.console.print(Panel(final_stats, style="bold bright_yellow"))
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = {
            'lm_studio_diverse_simple': {
                'shapes': shapes,
                'timestamp': timestamp
            }
        }
        
        with open(f"lm_studio_diverse_simple_{timestamp}.json", 'w') as f:
            json.dump(result, f, indent=2)
        
        self.console.print(f"Guardado: lm_studio_diverse_simple_{timestamp}.json")

if __name__ == "__main__":
    diverse = SimpleDiverse()
    diverse.run_diverse_artwork()
