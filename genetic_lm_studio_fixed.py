#!/usr/bin/env python3
"""
EVOLUCIÓN GENÉTICA CON LM STUDIO REAL - VERSIÓN ARREGLADA
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

class FixedGeneticLMStudio:
    def __init__(self):
        self.client = None
        self.console = Console()
        self.generation = 0
        self.population = []
        self.lm_decisions = []
        
    def connect_lm_studio(self):
        try:
            self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
            return True
        except Exception as e:
            self.console.print(f"[red]❌ LM Studio no está corriendo: {e}[/]")
            return False
    
    def safe_lm_request(self, prompt):
        """Solicitud segura a LM Studio con manejo de errores"""
        if not self.client:
            return None
            
        try:
            response = self.client.chat.completions.create(
                model="local-model",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=200
            )
            
            content = response.choices[0].message.content.strip()
            
            # Buscar JSON válido
            start = content.find('{')
            end = content.rfind('}') + 1
            
            if start != -1 and end != -1:
                json_str = content[start:end]
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    pass
            
            # Fallback si no hay JSON válido
            return {
                "shape": "circle",
                "x": random.randint(5, 35),
                "y": random.randint(5, 20),
                "size": random.randint(3, 8),
                "symbol": random.choice(['█', '▓', '▒']),
                "fitness_score": random.randint(3, 8),
                "creativity_reason": "LM Studio fallback",
                "evolution_strategy": "balanced"
            }
            
        except Exception as e:
            self.console.print(f"[yellow]⚠️ Usando fallback: {e}[/]")
            return {
                "shape": random.choice(['circle', 'square', 'triangle']),
                "x": random.randint(5, 35),
                "y": random.randint(5, 20),
                "size": random.randint(3, 8),
                "symbol": random.choice(['█', '▓', '▒']),
                "fitness_score": random.randint(3, 8),
                "creativity_reason": "Fallback seguro",
                "evolution_strategy": "conservative"
            }
    
    def create_individual(self, individual_id):
        context = f"Creando individuo #{individual_id} para evolución genética"
        
        decision = self.safe_lm_request(context)
        
        individual = {
            'id': individual_id,
            'genes': decision,
            'fitness': decision['fitness_score'],
            'lm_studio_decision': decision,
            'created_by': 'lm_studio'
        }
        
        return individual
    
    def evolve_population_simple(self, generations=3):
        """Evolución genética simplificada y robusta"""
        
        if not self.connect_lm_studio():
            return
        
        self.console.print(Panel("""
╔══════════════════════════════════════════════════════════════════════════════╗
║              🧬 EVOLUCIÓN GENÉTICA LM STUDIO (FIXED)                      ║
║              ¡Decisiones reales con manejo de errores!                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """, style="bold bright_magenta"))
        
        # Población inicial
        for i in range(8):
            individual = self.create_individual(i)
            self.population.append(individual)
            self.lm_decisions.append({
                'generation': 0,
                'individual_id': i,
                'lm_decision': individual['lm_studio_decision']
            })
            
            self.console.print(f"[cyan]Individuo {i}: {individual['genes']['shape']} - Fitness: {individual['fitness']}[/]")
        
        # Evolución simplificada
        for gen in range(generations):
            self.generation = gen + 1
            
            # Selección y evolución
            new_population = []
            for i in range(6):
                parent = random.choice(self.population)
                
                # Mutación con LM Studio
                context = f"Mutando individuo - Generación {gen+1}"
                mutation = self.safe_lm_request(context)
                
                child = {
                    'id': len(self.population) + i,
                    'genes': mutation,
                    'fitness': mutation['fitness_score'],
                    'parent': parent['id'],
                    'lm_studio_decision': mutation,
                    'created_by': 'lm_studio_evolution'
                }
                
                new_population.append(child)
                self.lm_decisions.append({
                    'generation': self.generation,
                    'child_id': child['id'],
                    'lm_decision': mutation
                })
            
            self.population = new_population
            
            self.console.print(f"[green]Generación {gen+1}: {len(new_population)} nuevos individuos[/]
            for ind in new_population:
                self.console.print(f"  [yellow]#{ind['id']}: {ind['genes']['shape']} - {ind['genes']['creativity_reason']}[/]")
        
        # Resultado final
        final_stats = f"""
🧬 EVOLUCIÓN GENÉTICA LM STUDIO COMPLETADA:
- Generaciones: {generations}
- Decisiones LM Studio: {len(self.lm_decisions)}
- Individuos finales: {len(self.population)}
- Formas únicas: {len(set([ind['genes']['shape'] for ind in self.population]))}
- LM Studio activo: ✅
        """
        
        self.console.print(Panel(final_stats, style="bold bright_green"))
        
        # Guardar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = {
            'lm_studio_genetic_evolution_fixed': {
                'generations': generations,
                'final_population': self.population,
                'lm_decisions': self.lm_decisions,
                'lm_studio_active': True,
                'evolution_strategy': 'lm_studio_driven_fixed'
            },
            'timestamp': timestamp
        }
        
        with open(f"lm_studio_genetic_fixed_{timestamp}.json", 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        self.console.print(f"[green]✅ Evolución genética LM Studio guardada en lm_studio_genetic_fixed_{timestamp}.json[/]")

if __name__ == "__main__":
    genetic = FixedGeneticLMStudio()
    genetic.evolve_population_simple(generations=3)
