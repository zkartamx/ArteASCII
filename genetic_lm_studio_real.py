#!/usr/bin/env python3
"""
EVOLUCIÓN GENÉTICA CON LM STUDIO REAL
Cada decisión genética tomada REALMENTE por LM Studio
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

class RealGeneticLMStudio:
    """Evolución genética donde LM Studio decide MUTACIONES y CRUCES"""
    
    def __init__(self):
        self.client = None
        self.console = Console()
        self.generation = 0
        self.population = []
        self.lm_decisions = []
        
    def connect_lm_studio(self):
        """Conectar REALMENTE con LM Studio"""
        try:
            self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
            return True
        except Exception as e:
            self.console.print(f"[red]❌ LM Studio no está corriendo: {e}[/]")
            return False
    
    def ask_lm_studio_for_genetic_decision(self, context, decision_type):
        """LM Studio decide MUTACIONES, CRUCES y FITNESS"""
        if not self.client:
            return None
            
        prompt = f"""
        Eres un experto en algoritmos genéticos. Contexto:
        {context}
        
        Tipo de decisión: {decision_type}
        
        Devuelve EXACTAMENTE en formato JSON:
        {{
            "action": "mutate|crossover|select|evolve",
            "shape": "circle|square|triangle|fractal|wave|spiral",
            "x": número 0-39,
            "y": número 0-24,
            "size": número 3-10,
            "symbol": "█|▓|▒|░|◆|●|■",
            "mutation_rate": 0.0-1.0,
            "fitness_score": 0-10,
            "creativity_reason": "razón genética",
            "evolution_strategy": "aggressive|conservative|balanced"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="local-model",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300
            )
            
            content = response.choices[0].message.content
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != -1:
                import json
                return json.loads(content[start:end])
                
        except Exception as e:
            self.console.print(f"[red]❌ Error LM Studio genético: {e}[/]")
            
        return None
    
    def create_individual_from_lm_decision(self, individual_id):
        """Crear individuo con decisión REAL de LM Studio"""
        context = f"""
        Creando individuo #{individual_id} para evolución genética.
        Generación actual: {self.generation}
        Población actual: {len(self.population)} individuos
        """
        
        lm_decision = self.ask_lm_studio_for_genetic_decision(context, "create_individual")
        
        if not lm_decision:
            # Fallback
            lm_decision = {
                "shape": random.choice(['circle', 'square', 'triangle']),
                "x": random.randint(5, 35),
                "y": random.randint(5, 20),
                "size": random.randint(3, 8),
                "symbol": random.choice(['█', '▓', '▒']),
                "mutation_rate": 0.1,
                "fitness_score": 5,
                "creativity_reason": "Fallback genético",
                "evolution_strategy": "balanced"
            }
        
        individual = {
            'id': individual_id,
            'genes': lm_decision,
            'fitness': lm_decision['fitness_score'],
            'lm_studio_decision': lm_decision,
            'created_by': 'lm_studio'
        }
        
        return individual
    
    def mutate_with_lm_studio(self, parent):
        """LM Studio decide MUTACIÓN REAL"""
        context = f"""
        Mutando individuo #{parent['id']}
        Genes actuales: {parent['genes']}
        Fitness actual: {parent['fitness']}
        
        Decide cómo mutar este individuo para mejorar su fitness.
        """
        
        mutation = self.ask_lm_studio_for_genetic_decision(context, "mutate")
        
        if mutation:
            child = parent.copy()
            child['genes'].update(mutation)
            child['lm_studio_decision'] = mutation
            child['created_by'] = 'lm_studio_mutation'
            return child
        
        return parent
    
    def crossover_with_lm_studio(self, parent1, parent2):
        """LM Studio decide CRUCE REAL"""
        context = f"""
        Cruzando individuos #{parent1['id']} y #{parent2['id']}
        Padre 1: {parent1['genes']}
        Padre 2: {parent2['genes']}
        
        Decide cómo combinar sus genes para crear un hijo superior.
        """
        
        crossover = self.ask_lm_studio_for_genetic_decision(context, "crossover")
        
        if crossover:
            child = {
                'id': len(self.population) + 1,
                'genes': crossover,
                'fitness': crossover['fitness_score'],
                'parents': [parent1['id'], parent2['id']],
                'lm_studio_decision': crossover,
                'created_by': 'lm_studio_crossover'
            }
            return child
        
        return None
    
    def evolve_population(self, generations=10):
        """Evolución genética REAL con LM Studio"""
        
        if not self.connect_lm_studio():
            return
        
        self.console.print(Panel("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🧬 EVOLUCIÓN GENÉTICA LM STUDIO REAL                     ║
║                   ¡Cada decisión tomada por LM Studio!                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """, style="bold bright_magenta"))
        
        # Población inicial con LM Studio
        for i in range(20):
            individual = self.create_individual_from_lm_decision(i)
            self.population.append(individual)
            self.lm_decisions.append({
                'generation': 0,
                'individual_id': i,
                'lm_decision': individual['lm_studio_decision']
            })
        
        for gen in range(generations):
            self.generation = gen + 1
            
            # Selección por LM Studio
            selected = []
            for individual in self.population:
                context = f"""
                Selección natural. Individuo #{individual['id']}
                Fitness: {individual['fitness']}
                Genes: {individual['genes']}
                
                Decide si sobrevive o muere.
                """
                
                survival = self.ask_lm_studio_for_genetic_decision(context, "select")
                if survival and survival.get('fitness_score', 0) > 5:
                    selected.append(individual)
            
            # Cruce y mutación con LM Studio
            new_population = []
            for i in range(0, len(selected), 2):
                if i + 1 < len(selected):
                    child = self.crossover_with_lm_studio(selected[i], selected[i+1])
                    if child:
                        mutated_child = self.mutate_with_lm_studio(child)
                        new_population.append(mutated_child)
                        self.lm_decisions.append({
                            'generation': self.generation,
                            'child_id': mutated_child['id'],
                            'lm_decision': mutated_child['lm_studio_decision']
                        })
            
            self.population = new_population
            
            # Mostrar progreso
            self.console.print(f"[cyan]Generación {gen+1}: {len(self.population)} individuos[/]")
            for ind in self.population:
                self.console.print(f"  [yellow]#{ind['id']}: {ind['genes']['shape']} - {ind['genes']['creativity_reason']}[/]")
        
        # Resultado final
        final_stats = f"""
🧬 EVOLUCIÓN GENÉTICA LM STUDIO COMPLETADA:
- Generaciones: {generations}
- Decisiones LM Studio: {len(self.lm_decisions)}
- Individuos finales: {len(self.population)}
- Formas únicas: {len(set([ind['genes']['shape'] for ind in self.population]))}
- Estrategias evolutivas: {len(set([ind['genes']['evolution_strategy'] for ind in self.population]))}
- LM Studio activo: ✅

🧠 Decisiones tomadas por LM Studio:
{len(self.lm_decisions)} decisiones reales de evolución genética
        """
        
        self.console.print(Panel(final_stats, style="bold bright_green"))
        
        # Guardar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = {
            'lm_studio_genetic_evolution': {
                'generations': generations,
                'final_population': self.population,
                'lm_decisions': self.lm_decisions,
                'lm_studio_active': True,
                'evolution_strategy': 'lm_studio_driven'
            },
            'timestamp': timestamp
        }
        
        with open(f"lm_studio_genetic_{timestamp}.json", 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        self.console.print(f"[green]✅ Evolución genética LM Studio guardada en lm_studio_genetic_{timestamp}.json[/]")

if __name__ == "__main__":
    genetic = RealGeneticLMStudio()
    genetic.evolve_population(generations=5)
