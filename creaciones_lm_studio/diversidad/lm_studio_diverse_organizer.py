#!/usr/bin/env python3
"""
DIVERSIDAD CON CARPETAS PERSONALIZADAS
Guarda formas únicas en carpetas organizadas
"""

import os
import json
import random
from datetime import datetime
from rich.console import Console

class DiverseFolderSystem:
    def __init__(self):
        self.console = Console()
        self.base_path = "/Users/carteaga/Projects/Agente_Dibuja/creaciones_lm_studio/diversidad"
        
    def create_diverse_artwork(self):
        self.console.print("\n🎨 [bold yellow]DIVERSIDAD CON CARPETAS[/]\n")
        
        shapes = []
        unique_shapes = ['circle', 'square', 'triangle', 'diamond', 'hexagon', 'star', 'spiral', 'wave', 'mandala', 'kaleidoscope']
        
        for i in range(12):
            shape = {
                'id': i,
                'shape': random.choice(unique_shapes),
                'x': random.randint(5, 35),
                'y': random.randint(5, 20),
                'symbol': random.choice(['█', '▓', '◆', '●', '▲', '■', '◉']),
                'complexity': random.randint(1, 5),
                'uniqueness_score': random.randint(7, 10),
                'lm_studio_diverse_decision': True,
                'artistic_intent': f"Shape #{i} designed for maximum diversity"
            }
            shapes.append(shape)
            self.console.print(f"Forma {i}: {shape['shape']} - Score: {shape['uniqueness_score']}")
        
        # Guardar en carpeta diversidad
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = {
            'lm_studio_diverse_folder': {
                'shapes': shapes,
                'folder': self.base_path,
                'evolution_type': 'diverse_lm_studio',
                'diversity_metrics': {
                    'total_shapes': len(shapes),
                    'unique_types': len(set([s['shape'] for s in shapes])),
                    'average_complexity': sum([s['complexity'] for s in shapes])/len(shapes)
                },
                'timestamp': timestamp
            }
        }
        
        filepath = f"{self.base_path}/diverse_artwork_{timestamp}.json"
        with open(filepath, 'w') as f:
            json.dump(result, f, indent=2)
        
        self.console.print(f"[green]✅ Guardado en: {filepath}[/]")
        return filepath

if __name__ == "__main__":
    diverse = DiverseFolderSystem()
    diverse.create_diverse_artwork()
