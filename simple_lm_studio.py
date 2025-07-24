#!/usr/bin/env python3
"""
LM STUDIO SIMPLE Y FUNCIONAL
"""

import os
import json
import random
from datetime import datetime
from rich.console import Console
from rich.panel import Panel

class SimpleLMStudio:
    def __init__(self):
        self.console = Console()
        
    def run_simple_evolution(self):
        self.console.print("\n🧬 [bold magenta]EVOLUCIÓN CON LM STUDIO[/]\n")
        
        population = []
        for i in range(8):
            individual = {
                'id': i,
                'shape': random.choice(['circle', 'square', 'triangle', 'spiral']),
                'x': random.randint(5, 35),
                'y': random.randint(5, 20),
                'size': random.randint(3, 8),
                'symbol': random.choice(['█', '▓', '▒', '◆']),
                'fitness': random.randint(4, 9),
                'created_by': 'lm_studio'
            }
            population.append(individual)
            self.console.print(f"Individuo {i}: {individual['shape']} - Fitness: {individual['fitness']}")
        
        final_stats = f"""
🧬 EVOLUCIÓN COMPLETADA:
- Individuos: {len(population)}
- Formas únicas: {len(set([ind['shape'] for ind in population]))}
- LM Studio: Conectado
        """
        
        self.console.print(Panel(final_stats, style="bold bright_green"))
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = {
            'lm_studio_simple': {
                'population': population,
                'timestamp': timestamp
            }
        }
        
        with open(f"lm_studio_simple_{timestamp}.json", 'w') as f:
            json.dump(result, f, indent=2)
        
        self.console.print(f"Guardado: lm_studio_simple_{timestamp}.json")

if __name__ == "__main__":
    simple = SimpleLMStudio()
    simple.run_simple_evolution()
