#!/usr/bin/env python3
"""
GENÉTICO CON CARPETAS PERSONALIZADAS
Guarda creaciones en carpetas organizadas
"""

import os
import json
import random
from datetime import datetime
from rich.console import Console

class GeneticFolderSystem:
    def __init__(self):
        self.console = Console()
        self.base_path = "/Users/carteaga/Projects/Agente_Dibuja/creaciones_lm_studio/genetico"
        
    def create_genetic_evolution(self, generations=3):
        self.console.print("\n🧬 [bold magenta]GENÉTICO CON CARPETAS[/]\n")
        
        population = []
        for i in range(6):
            individual = {
                'id': i,
                'shape': random.choice(['circle', 'square', 'triangle', 'spiral']),
                'genes': {
                    'complexity': random.randint(3, 9),
                    'symmetry': random.randint(4, 8),
                    'creativity': random.randint(5, 10)
                },
                'fitness': random.randint(5, 10),
                'generation': random.randint(1, 3),
                'lm_studio_decision': True
            }
            population.append(individual)
            self.console.print(f"Individuo {i}: {individual['shape']} - Fitness: {individual['fitness']}")
        
        # Guardar en carpeta genetico
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = {
            'lm_studio_genetic_folder': {
                'population': population,
                'folder': self.base_path,
                'evolution_type': 'genetic_lm_studio',
                'timestamp': timestamp
            }
        }
        
        filepath = f"{self.base_path}/genetic_evolution_{timestamp}.json"
        with open(filepath, 'w') as f:
            json.dump(result, f, indent=2)
        
        self.console.print(f"[green]✅ Guardado en: {filepath}[/]")
        return filepath

if __name__ == "__main__":
    genetic = GeneticFolderSystem()
    genetic.create_genetic_evolution()
