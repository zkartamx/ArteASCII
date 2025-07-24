#!/usr/bin/env python3
"""
Agente Dibuja - Evolución Genética
Sistema de arte ASCII con evolución genética real
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
from collections import defaultdict, deque

class GeneticShape:
    """Genes de una forma ASCII"""
    
    def __init__(self, genes=None):
        self.genes = genes or {
            'type': random.choice(['circle', 'square', 'triangle', 'star', 'spiral', 'fractal']),
            'size': random.randint(3, 8),
            'density': random.uniform(0.3, 1.0),
            'symmetry': random.choice(['radial', 'bilateral', 'asymmetric']),
            'complexity': random.randint(1, 5),
            'mutation_rate': random.uniform(0.1, 0.3),
            'fitness': 0.0
        }
    
    def mutate(self):
        """Mutación genética"""
        if random.random() < self.genes['mutation_rate']:
            gene = random.choice(['size', 'density', 'complexity'])
            if gene == 'size':
                self.genes['size'] = max(2, self.genes['size'] + random.choice([-1, 1]))
            elif gene == 'density':
                self.genes['density'] = max(0.1, min(1.0, self.genes['density'] + random.uniform(-0.2, 0.2)))
            elif gene == 'complexity':
                self.genes['complexity'] = max(1, min(5, self.genes['complexity'] + random.choice([-1, 1])))
    
    def crossover(self, other):
        """Cruce genético"""
        child_genes = self.genes.copy()
        crossover_point = random.randint(1, 5)
        keys = list(self.genes.keys())
        
        for i, key in enumerate(keys):
            if i >= crossover_point:
                child_genes[key] = other.genes[key]
        
        return GeneticShape(child_genes)
    
    def calculate_fitness(self, canvas, position, symbol):
        """Calcular fitness basado en estética"""
        x, y = position
        
        # Complejidad visual
        complexity_score = self.genes['complexity'] * 0.3
        
        # Simetría
        symmetry_score = self.calculate_symmetry(canvas, x, y) * 0.4
        
        # Densidad balanceada
        density_score = min(1.0, self.count_neighbors(canvas, x, y) / 10) * 0.3
        
        self.genes['fitness'] = complexity_score + symmetry_score + density_score
        return self.genes['fitness']
    
    def calculate_symmetry(self, canvas, x, y):
        """Calcular simetría de la forma"""
        symmetry = 0
        radius = self.genes['size']
        
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if 0 <= x+dx < len(canvas.grid[0]) and 0 <= y+dy < len(canvas.grid):
                    mirror_x = x - dx
                    mirror_y = y - dy
                    
                    if 0 <= mirror_x < len(canvas.grid[0]) and 0 <= mirror_y < len(canvas.grid):
                        if canvas.grid[y+dy][x+dx] == canvas.grid[mirror_y][mirror_x]:
                            symmetry += 1
        
        return symmetry / max(1, (radius * 2 + 1) ** 2)
    
    def count_neighbors(self, canvas, x, y):
        """Contar vecinos para balance"""
        count = 0
        radius = 2
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if 0 <= x+dx < len(canvas.grid[0]) and 0 <= y+dy < len(canvas.grid):
                    if canvas.grid[y+dy][x+dx] != ' ':
                        count += 1
        return count

class EvolutionaryCanvas:
    """Canvas con evolución genética"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]
        self.population = []
        self.generation = 0
        self.fitness_history = []
        
    def initialize_population(self, size=20):
        """Inicializar población genética"""
        for _ in range(size):
            self.population.append(GeneticShape())
    
    def evolve_population(self):
        """Evolución de una generación"""
        # Selección natural
        self.population.sort(key=lambda x: x.genes['fitness'], reverse=True)
        survivors = self.population[:len(self.population)//2]
        
        # Reproducción
        offspring = []
        for _ in range(len(self.population) - len(survivors)):
            parent1 = random.choice(survivors)
            parent2 = random.choice(survivors)
            child = parent1.crossover(parent2)
            child.mutate()
            offspring.append(child)
        
        self.population = survivors + offspring
        self.generation += 1
        
        # Registrar fitness promedio
        avg_fitness = sum(p.genes['fitness'] for p in self.population) / len(self.population)
        self.fitness_history.append(avg_fitness)
    
    def draw_genetic_shape(self, shape: GeneticShape, position, symbol):
        """Dibujar forma basada en genes"""
        x, y = position
        shape_type = shape.genes['type']
        size = shape.genes['size']
        
        if shape_type == 'circle':
            return self.draw_circle(x, y, size, symbol)
        elif shape_type == 'square':
            return self.draw_square(x, y, size, symbol)
        elif shape_type == 'triangle':
            return self.draw_triangle(x, y, size, symbol)
        elif shape_type == 'star':
            return self.draw_star(x, y, size, symbol)
        elif shape_type == 'spiral':
            return self.draw_spiral(x, y, size, symbol)
        elif shape_type == 'fractal':
            return self.draw_fractal(x, y, size, symbol)
    
    def draw_circle(self, center_x, center_y, radius, symbol):
        points = []
        for angle in range(0, 360, 2):
            rad = math.radians(angle)
            x = int(center_x + radius * math.cos(rad))
            y = int(center_y + radius * math.sin(rad))
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y][x] = symbol
                points.append((x, y))
        return points
    
    def draw_square(self, x, y, size, symbol):
        points = []
        for i in range(size):
            for j in range(size):
                if 0 <= x+i < self.width and 0 <= y+j < self.height:
                    if i == 0 or i == size-1 or j == 0 or j == size-1:
                        self.grid[y+j][x+i] = symbol
                        points.append((x+i, y+j))
        return points
    
    def draw_triangle(self, x, y, size, symbol):
        points = []
        for row in range(size):
            spaces = size - row - 1
            stars = 2 * row + 1
            for col in range(stars):
                draw_x = x + spaces + col
                draw_y = y + row
                if 0 <= draw_x < self.width and 0 <= draw_y < self.height:
                    self.grid[draw_y][draw_x] = symbol
                    points.append((draw_x, draw_y))
        return points
    
    def draw_star(self, center_x, center_y, size, symbol):
        points = []
        for i in range(10):
            angle = 2 * math.pi * i / 10
            r = size if i % 2 == 0 else size // 2
            x = int(center_x + r * math.cos(angle))
            y = int(center_y + r * math.sin(angle))
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y][x] = symbol
                points.append((x, y))
        return points
    
    def draw_spiral(self, center_x, center_y, size, symbol):
        points = []
        for i in range(size * 8):
            angle = 0.2 * i
            r = 0.1 * i
            x = int(center_x + r * math.cos(angle))
            y = int(center_y + r * math.sin(angle))
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y][x] = symbol
                points.append((x, y))
        return points
    
    def draw_fractal(self, center_x, center_y, size, symbol):
        """Fractal recursivo"""
        points = []
        
        def recursive_fractal(x, y, current_size, depth):
            if depth <= 0 or current_size < 1:
                return
            
            # Dibujar forma base
            for dx in range(-current_size, current_size + 1):
                for dy in range(-current_size, current_size + 1):
                    if abs(dx) + abs(dy) <= current_size:
                        new_x = x + dx
                        new_y = y + dy
                        if 0 <= new_x < self.width and 0 <= new_y < self.height:
                            self.grid[new_y][new_x] = symbol
                            points.append((new_x, new_y))
            
            # Recursión para detalles
            if depth > 1:
                for angle in range(0, 360, 90):
                    rad = math.radians(angle)
                    new_x = x + int(current_size * 0.7 * math.cos(rad))
                    new_y = y + int(current_size * 0.7 * math.sin(rad))
                    recursive_fractal(new_x, new_y, current_size // 2, depth - 1)
        
        recursive_fractal(center_x, center_y, size, 3)
        return points

class GeneticArtist:
    """Agente con evolución genética"""
    
    def __init__(self, name: str, client, canvas):
        self.name = name
        self.client = client
        self.canvas = canvas
        self.evolution_log = []
        self.best_shapes = []
    
    def create_evolutionary_art(self, generation: int) -> dict:
        """Crear arte con evolución genética"""
        # Evolucionar población
        self.canvas.evolve_population()
        
        # Seleccionar mejor forma
        best_shape = max(self.canvas.population, key=lambda x: x.genes['fitness'])
        
        # Posición evolutiva
        positions = [
            (10, 8), (25, 8), (15, 15), (30, 12), (5, 18),
            (20, 5), (35, 20), (8, 12), (28, 18), (12, 22),
            (18, 3), (32, 5), (7, 15), (22, 20), (33, 8)
        ]
        
        pos_x, pos_y = positions[generation % len(positions)]
        
        # Símbolos evolutivos
        symbols = ["█", "▓", "▒", "░", "▄", "▀", "▌", "▐", "•", "+", "■", "◆"]
        symbol = symbols[generation % len(symbols)]
        
        # Calcular fitness
        fitness = best_shape.calculate_fitness(self.canvas, (pos_x, pos_y), symbol)
        
        # Dibujar forma
        points = self.canvas.draw_genetic_shape(best_shape, (pos_x, pos_y), symbol)
        
        return {
            "generation": generation,
            "shape_type": best_shape.genes['type'],
            "genes": best_shape.genes,
            "fitness": fitness,
            "position": (pos_x, pos_y),
            "symbol": symbol,
            "points": len(points),
            "evolution_stage": self.get_evolution_stage()
        }
    
    def get_evolution_stage(self) -> str:
        """Determinar etapa evolutiva"""
        avg_fitness = sum(p.genes['fitness'] for p in self.canvas.population) / len(self.canvas.population)
        
        if avg_fitness < 0.3:
            return "🧬 Etapa Primordial"
        elif avg_fitness < 0.6:
            return "🔄 Etapa Adaptativa"
        elif avg_fitness < 0.8:
            return "⚡ Etapa de Optimización"
        else:
            return "🌟 Etapa Maestra"

class GeneticEvolutionApp:
    """Aplicación de evolución genética"""
    
    def __init__(self):
        self.console = Console()
        self.canvas = EvolutionaryCanvas(40, 25)
        self.client = None
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def create_banner(self):
        return """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          🧬 EVOLUCIÓN GENÉTICA                              ║
║                    Arte ASCII con Algoritmos Genéticos                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
    
    def display_canvas(self):
        lines = []
        for row in self.canvas.grid:
            colored_line = ""
            for char in row:
                if char != ' ':
                    colored_line += f'[bold bright_green]{char}[/]'
                else:
                    colored_line += ' '
            lines.append(colored_line)
        return '\n'.join(lines)
    
    def display_evolution_stats(self, generation_data):
        """Mostrar estadísticas evolutivas"""
        table = Table(title="📊 Estadísticas Evolutivas")
        table.add_column("Métrica", style="cyan")
        table.add_column("Valor", style="magenta")
        
        table.add_row("Generación", str(generation_data['generation']))
        table.add_row("Tipo de Forma", generation_data['shape_type'])
        table.add_row("Fitness", f"{generation_data['fitness']:.3f}")
        table.add_row("Complejidad", str(generation_data['genes']['complexity']))
        table.add_row("Densidad", f"{generation_data['genes']['density']:.2f}")
        table.add_row("Evolución", generation_data['evolution_stage'])
        
        return table
    
    def run_evolution(self, generations=15):
        self.clear_screen()
        
        self.console.print(Panel(self.create_banner(), style="bold bright_magenta"))
        
        try:
            self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
        except Exception as e:
            print(f"Error: {e}")
            return
        
        # Inicializar población
        self.canvas.initialize_population()
        
        artist = GeneticArtist("🧬 Genetic_Master", self.client, self.canvas)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            task = progress.add_task("Evolucionando arte...", total=generations)
            
            for gen in range(generations):
                self.clear_screen()
                
                evolution_data = artist.create_evolutionary_art(gen)
                
                self.console.print(Panel(self.create_banner(), style="bold bright_magenta"))
                
                canvas_display = self.display_canvas()
                self.console.print(Panel(canvas_display, title=f"🧬 Generación {gen + 1}"))
                
                stats_table = self.display_evolution_stats(evolution_data)
                self.console.print(stats_table)
                
                # Log evolutivo
                self.console.print(Panel(
                    f"🧬 ADN Evolutivo: {evolution_data['genes']}",
                    title="📋 Genoma"
                ))
                
                progress.update(task, advance=1)
                time.sleep(1.5)
        
        # Resultado final evolutivo
        self.clear_screen()
        self.console.print(Panel(self.create_banner(), style="bold bright_green"))
        
        final_canvas = self.display_canvas()
        self.console.print(Panel(final_canvas, title="🧬 Evolución Final"))
        
        # Estadísticas evolutivas finales
        final_stats = f"""🧬 Evolución Completada:
- Generaciones: {generations}
- Población final: {len(self.canvas.population)}
- Fitness promedio: {sum(p.genes['fitness'] for p in self.canvas.population)/len(self.canvas.population):.3f}
- Mejor fitness: {max(p.genes['fitness'] for p in self.canvas.population):.3f}
- Formas evolucionadas: {len(set(p.genes['type'] for p in self.canvas.population))}
- ADN optimizado: ✅"""
        
        self.console.print(Panel(final_stats, title="📈 Análisis Evolutivo Final"))
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = {
            'evolutionary_artwork': [''.join(row) for row in self.canvas.grid],
            'generations': generations,
            'final_population': [
                {
                    'genes': shape.genes,
                    'fitness': shape.genes['fitness'],
                    'type': shape.genes['type']
                }
                for shape in self.canvas.population
            ],
            'fitness_history': self.canvas.fitness_history,
            'timestamp': timestamp
        }
        
        with open(f"genetic_evolution_{timestamp}.json", 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        self.console.print(f"[green]✅ Evolución genética guardada en genetic_evolution_{timestamp}.json[/]")

if __name__ == "__main__":
    app = GeneticEvolutionApp()
    
    try:
        app.run_evolution(generations=15)
    except KeyboardInterrupt:
        print("\n[red]⏹️ Evolución interrumpida[/]")
    except Exception as e:
        print(f"\n[red]❌ Error evolutivo: {e}[/]")
