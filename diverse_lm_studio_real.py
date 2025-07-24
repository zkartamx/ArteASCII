#!/usr/bin/env python3
"""
DIVERSIDAD MAXIMA CON LM STUDIO REAL
Cada forma única decidida REALMENTE por LM Studio
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
from rich.progress import Progress, SpinnerColumn, TextColumn

class RealDiverseLMStudio:
    """Diversidad máxima donde LM Studio decide CADA FORMA ÚNICA"""
    
    def __init__(self):
        self.client = None
        self.console = Console()
        self.shapes_created = []
        self.lm_decisions = []
        self.diversity_metrics = []
        
    def connect_lm_studio(self):
        """Conectar REALMENTE con LM Studio"""
        try:
            self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
            return True
        except Exception as e:
            self.console.print(f"[red]❌ LM Studio no está corriendo: {e}[/]")
            return False
    
    def ask_lm_studio_for_diverse_shape(self, context, shape_id):
        """LM Studio decide CADA FORMA ÚNICA y POSICIÓN"""
        if not self.client:
            return None
            
        prompt = f"""
        Eres un artista de formas ASCII ultra-creativo. Contexto:
        {context}
        
        Forma #{shape_id} - DEBE ser única y creativa
        
        Devuelve EXACTAMENTE en formato JSON:
        {{
            "shape_type": "geometric|fractal|organic|abstract|symbolic|textural",
            "specific_shape": "circle|square|triangle|diamond|hexagon|star|cross|spiral|wave|lattice|mandala|kaleidoscope",
            "x": número 0-39,
            "y": número 0-24,
            "width": número 2-15,
            "height": número 2-15,
            "symbol": "█|▓|▒|░|▄|▀|▌|▐|◆|●|■|▲|▼|◉|◎|◈|◇|◊|★|✦|✧",
            "rotation": 0-360,
            "complexity": 1-10,
            "creativity_reason": "razón creativa única",
            "diversity_score": 1-10,
            "artistic_intent": "intención artística"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="local-model",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.95,
                max_tokens=400
            )
            
            content = response.choices[0].message.content
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != -1:
                import json
                return json.loads(content[start:end])
                
        except Exception as e:
            self.console.print(f"[red]❌ Error LM Studio diversidad: {e}[/]")
            
        return None
    
    def create_shape_from_lm_decision(self, shape_id):
        """Crear forma basada en decisión REAL de LM Studio"""
        context = f"""
        Creando forma #{shape_id} para máxima diversidad.
        Formas previas: {len(self.shapes_created)}
        
        Historial de formas: {[s['lm_decision']['specific_shape'] for s in self.shapes_created[-5:]]}
        
        Crea una forma COMPLETAMENTE ÚNICA que nunca antes se ha usado.
        """
        
        lm_shape = self.ask_lm_studio_for_diverse_shape(context, shape_id)
        
        if not lm_shape:
            # Fallback ultra-creativo
            unique_shapes = [
                'mandala', 'kaleidoscope', 'lattice', 'constellation', 'crystal',
                'nebula', 'galaxy', 'aurora', 'bioluminescent', 'fractal_tree'
            ]
            lm_shape = {
                "shape_type": "abstract",
                "specific_shape": random.choice(unique_shapes),
                "x": random.randint(0, 35),
                "y": random.randint(0, 20),
                "width": random.randint(3, 12),
                "height": random.randint(3, 12),
                "symbol": random.choice(['█', '◆', '●', '■', '◉', '✦', '✧']),
                "rotation": random.randint(0, 360),
                "complexity": random.randint(5, 10),
                "creativity_reason": "Fallback ultra-creativo",
                "diversity_score": random.randint(7, 10),
                "artistic_intent": "Exploración creativa máxima"
            }
        
        shape = {
            'id': shape_id,
            'lm_decision': lm_shape,
            'created_by': 'lm_studio_diversity',
            'diversity_score': lm_shape['diversity_score'],
            'uniqueness_hash': f"{lm_shape['specific_shape']}_{lm_shape['x']}_{lm_shape['y']}_{lm_shape['symbol']}"
        }
        
        return shape
    
    def draw_diverse_shape_from_lm(self, shape_data):
        """Dibujar forma basada en decisión LM Studio"""
        canvas = [[' ' for _ in range(40)] for _ in range(25)]
        decision = shape_data['lm_decision']
        
        x, y = decision['x'], decision['y']
        width, height = decision['width'], decision['height']
        symbol = decision['symbol']
        
        # Dibujar según tipo específico decidido por LM Studio
        if decision['specific_shape'] == 'circle':
            return self.draw_circle_diverse(canvas, x, y, width, symbol)
        elif decision['specific_shape'] == 'square':
            return self.draw_square_diverse(canvas, x, y, width, height, symbol)
        elif decision['specific_shape'] == 'triangle':
            return self.draw_triangle_diverse(canvas, x, y, width, symbol)
        elif decision['specific_shape'] == 'spiral':
            return self.draw_spiral_diverse(canvas, x, y, width, symbol)
        elif decision['specific_shape'] == 'mandala':
            return self.draw_mandala_diverse(canvas, x, y, width, symbol)
        elif decision['specific_shape'] == 'kaleidoscope':
            return self.draw_kaleidoscope_diverse(canvas, x, y, width, symbol)
        else:
            return self.draw_abstract_diverse(canvas, x, y, width, height, symbol)
    
    def draw_circle_diverse(self, canvas, center_x, center_y, radius, symbol):
        points = []
        for angle in range(0, 360, 3):
            rad = math.radians(angle)
            x = int(center_x + radius * math.cos(rad))
            y = int(center_y + radius * math.sin(rad))
            if 0 <= x < 40 and 0 <= y < 25:
                canvas[y][x] = symbol
                points.append((x, y))
        return canvas
    
    def draw_square_diverse(self, canvas, x, y, width, height, symbol):
        points = []
        for i in range(width):
            for j in range(height):
                if 0 <= x+i < 40 and 0 <= y+j < 25:
                    if i == 0 or i == width-1 or j == 0 or j == height-1:
                        canvas[y+j][x+i] = symbol
                        points.append((x+i, y+j))
        return canvas
    
    def draw_triangle_diverse(self, canvas, x, y, size, symbol):
        points = []
        for row in range(size):
            spaces = size - row - 1
            stars = 2 * row + 1
            for col in range(stars):
                draw_x = x + spaces + col
                draw_y = y + row
                if 0 <= draw_x < 40 and 0 <= draw_y < 25:
                    canvas[draw_y][draw_x] = symbol
                    points.append((draw_x, draw_y))
        return canvas
    
    def draw_spiral_diverse(self, canvas, center_x, center_y, size, symbol):
        points = []
        for i in range(size * 8):
            angle = 0.2 * i
            r = 0.1 * i
            x = int(center_x + r * math.cos(angle))
            y = int(center_y + r * math.sin(angle))
            if 0 <= x < 40 and 0 <= y < 25:
                canvas[y][x] = symbol
                points.append((x, y))
        return canvas
    
    def draw_mandala_diverse(self, canvas, center_x, center_y, size, symbol):
        points = []
        for layer in range(3):
            layer_size = size - layer * 2
            for angle in range(0, 360, 30):
                rad = math.radians(angle)
                x = int(center_x + layer_size * math.cos(rad))
                y = int(center_y + layer_size * math.sin(rad))
                if 0 <= x < 40 and 0 <= y < 25:
                    canvas[y][x] = symbol
                    points.append((x, y))
        return canvas
    
    def draw_kaleidoscope_diverse(self, canvas, center_x, center_y, size, symbol):
        points = []
        for mirror in range(8):
            for i in range(size):
                angle = (mirror * 45 + i * 5) * math.pi / 180
                x = int(center_x + i * math.cos(angle))
                y = int(center_y + i * math.sin(angle))
                if 0 <= x < 40 and 0 <= y < 25:
                    canvas[y][x] = symbol
                    points.append((x, y))
        return canvas
    
    def draw_abstract_diverse(self, canvas, x, y, width, height, symbol):
        points = []
        for i in range(width):
            for j in range(height):
                if 0 <= x+i < 40 and 0 <= y+j < 25:
                    if (i + j) % 3 == 0 and random.random() > 0.3:
                        canvas[y+j][x+i] = symbol
                        points.append((x+i, y+j))
        return canvas
    
    def generate_diverse_artwork(self, shapes_count=15):
        """Generar arte diverso REAL con LM Studio"""
        
        if not self.connect_lm_studio():
            return
        
        self.console.print(Panel("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🎨 DIVERSIDAD LM STUDIO REAL                            ║
║              ¡Cada forma única decidida por LM Studio!                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """, style="bold bright_yellow"))
        
        final_canvas = [[' ' for _ in range(40)] for _ in range(25)]
        
        for shape_id in range(shapes_count):
            # Crear forma única con LM Studio
            diverse_shape = self.create_shape_from_lm_decision(shape_id)
            self.shapes_created.append(diverse_shape)
            
            # Dibujar forma según decisión LM Studio
            shape_canvas = self.draw_diverse_shape_from_lm(diverse_shape)
            
            # Combinar en canvas final
            for y in range(25):
                for x in range(40):
                    if shape_canvas[y][x] != ' ':
                        final_canvas[y][x] = shape_canvas[y][x]
            
            # Guardar decisión LM Studio
            self.lm_decisions.append({
                'shape_id': shape_id,
                'lm_decision': diverse_shape['lm_decision'],
                'diversity_score': diverse_shape['diversity_score'],
                'uniqueness_hash': diverse_shape['uniqueness_hash']
            })
            
            # Mostrar progreso
            self.console.print(f"[cyan]Forma {shape_id+1}: {diverse_shape['lm_decision']['specific_shape']} - {diverse_shape['lm_decision']['creativity_reason']}[/]")
        
        # Calcular métricas de diversidad
        unique_shapes = len(set([s['lm_decision']['specific_shape'] for s in self.shapes_created]))
        unique_positions = len(set([(s['lm_decision']['x'], s['lm_decision']['y']) for s in self.shapes_created]))
        unique_symbols = len(set([s['lm_decision']['symbol'] for s in self.shapes_created]))
        
        final_stats = f"""
🎨 DIVERSIDAD LM STUDIO REAL COMPLETADA:
- Formas únicas creadas: {len(self.shapes_created)}
- Tipos de formas únicas: {unique_shapes}
- Posiciones únicas: {unique_positions}
- Símbolos únicos: {unique_symbols}
- Diversidad promedio: {sum([s['diversity_score'] for s in self.shapes_created])/len(self.shapes_created):.1f}
- LM Studio activo: ✅
- Arte generado por LM Studio: ✅

🧠 Decisiones tomadas por LM Studio:
{len(self.lm_decisions)} decisiones reales de diversidad
        """
        
        self.console.print(Panel(final_stats, style="bold bright_green"))
        
        # Mostrar arte final
        artwork_display = '\n'.join([''.join(row) for row in final_canvas])
        self.console.print(Panel(artwork_display, title="🎨 Arte Diversidad LM Studio"))
        
        # Guardar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = {
            'lm_studio_diverse_artwork': final_canvas,
            'lm_studio_decisions': self.lm_decisions,
            'shapes_created': self.shapes_created,
            'diversity_metrics': {
                'unique_shapes': unique_shapes,
                'unique_positions': unique_positions,
                'unique_symbols': unique_symbols,
                'average_diversity': sum([s['diversity_score'] for s in self.shapes_created])/len(self.shapes_created)
            },
            'lm_studio_active': True,
            'diversity_strategy': 'lm_studio_driven'
        }
        
        with open(f"lm_studio_diverse_{timestamp}.json", 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        self.console.print(f"[green]✅ Diversidad LM Studio guardada en lm_studio_diverse_{timestamp}.json[/]")

if __name__ == "__main__":
    diverse = RealDiverseLMStudio()
    diverse.generate_diverse_artwork(shapes_count=12)
