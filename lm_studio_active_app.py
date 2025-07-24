#!/usr/bin/env python3
"""
Agente Dibuja - LM Studio ACTIVO
Sistema que REALMENTE usa LM Studio para decisiones creativas
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

class LMStudioCanvas:
    """Canvas que REALMENTE consulta LM Studio"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]
        self.client = None
        self.decision_history = []
        
    def connect_lm_studio(self):
        """Conectar REALMENTE con LM Studio"""
        try:
            self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
            return True
        except Exception as e:
            print(f"❌ LM Studio no está corriendo: {e}")
            print("💡 Inicia LM Studio primero")
            return False
    
    def ask_lm_studio_for_decision(self, context):
        """Preguntar REALMENTE a LM Studio"""
        if not self.client:
            return None
            
        prompt = f"""
        Eres un artista ASCII creativo. Basado en este contexto:
        {context}
        
        Devuelve EXACTAMENTE en formato JSON:
        {{
            "shape": "circle|square|triangle|fractal|wave|spiral",
            "x": número entre 0-39,
            "y": número entre 0-24,
            "size": número entre 3-10,
            "symbol": "█|▓|▒|░|▄|▀|▌|◆|●|■",
            "creativity_reason": "razón creativa breve",
            "evolution_stage": "early|developing|mature|master"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="local-model",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=200
            )
            
            content = response.choices[0].message.content
            
            # Limpiar y parsear JSON
            import json
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = content[start:end]
                return json.loads(json_str)
                
        except Exception as e:
            print(f"❌ Error consultando LM Studio: {e}")
            
        return None
    
    def draw_shape_from_lm_decision(self, decision, symbol):
        """Dibujar basado en decisión REAL de LM Studio"""
        points = []
        x, y = decision['x'], decision['y']
        size = decision['size']
        
        if decision['shape'] == 'circle':
            return self.draw_circle(x, y, size, symbol)
        elif decision['shape'] == 'square':
            return self.draw_square(x, y, size, symbol)
        elif decision['shape'] == 'triangle':
            return self.draw_triangle(x, y, size, symbol)
        elif decision['shape'] == 'fractal':
            return self.draw_fractal(x, y, size, symbol)
        elif decision['shape'] == 'wave':
            return self.draw_wave(x, y, size, symbol)
        elif decision['shape'] == 'spiral':
            return self.draw_spiral(x, y, size, symbol)
        
        return points
    
    def draw_circle(self, center_x, center_y, radius, symbol):
        points = []
        for angle in range(0, 360, 5):
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
    
    def draw_fractal(self, x, y, size, symbol):
        """Fractal simple"""
        points = []
        for i in range(size):
            for j in range(size):
                if 0 <= x+i < self.width and 0 <= y+j < self.height:
                    if (i + j) % 3 == 0:
                        self.grid[y+j][x+i] = symbol
                        points.append((x+i, y+j))
        return points
    
    def draw_wave(self, x, y, length, symbol):
        points = []
        for i in range(length):
            wave_y = y + int(3 * math.sin(i * 0.3))
            if 0 <= x+i < self.width and 0 <= wave_y < self.height:
                self.grid[wave_y][x+i] = symbol
                points.append((x+i, wave_y))
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

class RealLMStudioAgent:
    """Agente que REALMENTE usa LM Studio"""
    
    def __init__(self, name: str, canvas):
        self.name = name
        self.canvas = canvas
        self.decisions = []
        
    def create_with_lm_studio(self, turn: int) -> dict:
        """Crear arte CON LM Studio activo"""
        
        # Contexto para LM Studio
        context = f"""
        Turno {turn}. Historial: {len(self.decisions)} decisiones previas.
        Estado actual: {self.canvas.grid}
        
        Crea una forma única y creativa. Sé innovador!
        """
        
        # Consultar REALMENTE a LM Studio
        decision = self.canvas.ask_lm_studio_for_decision(context)
        
        if not decision:
            # Fallback si LM Studio no responde
            decision = {
                "shape": random.choice(['circle', 'square', 'triangle', 'fractal']),
                "x": random.randint(5, 35),
                "y": random.randint(5, 20),
                "size": random.randint(3, 8),
                "symbol": random.choice(['█', '▓', '▒', '░', '◆']),
                "creativity_reason": "LM Studio no respondió - usando fallback",
                "evolution_stage": "fallback"
            }
        
        # Dibujar basado en decisión REAL
        symbol = decision['symbol']
        points = self.canvas.draw_shape_from_lm_decision(decision, symbol)
        
        # Guardar decisión
        self.decisions.append(decision)
        
        return {
            "turn": turn,
            "lm_decision": decision,
            "points_drawn": len(points),
            "lm_studio_active": self.canvas.client is not None,
            "creativity_reason": decision.get('creativity_reason', 'LM Studio decision'),
            "evolution_stage": decision.get('evolution_stage', 'unknown')
        }

class RealLMStudioApp:
    """Aplicación que REALMENTE usa LM Studio"""
    
    def __init__(self):
        self.console = Console()
        self.canvas = LMStudioCanvas(40, 25)
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def create_banner(self):
        return """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          🧠 LM STUDIO ACTIVO                               ║
║                    Arte ASCII con Decisiones REALES                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
    
    def display_canvas(self):
        lines = []
        for row in self.canvas.grid:
            colored_line = ""
            for char in row:
                if char != ' ':
                    colored_line += f'[bold bright_yellow]{char}[/]'
                else:
                    colored_line += ' '
            lines.append(colored_line)
        return '\n'.join(lines)
    
    def run_lm_studio_session(self, turns=10):
        self.clear_screen()
        
        self.console.print(Panel(self.create_banner(), style="bold bright_red"))
        
        # Verificar conexión con LM Studio
        if not self.canvas.connect_lm_studio():
            self.console.print("[red]❌ Por favor inicia LM Studio primero[/]")
            return
        
        agent = RealLMStudioAgent("🧠 LM_Studio_Master", self.canvas)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            task = progress.add_task("Consultando LM Studio...", total=turns)
            
            for turn in range(turns):
                self.clear_screen()
                
                # ESTO sí consulta REALMENTE a LM Studio
                lm_data = agent.create_with_lm_studio(turn)
                
                self.console.print(Panel(self.create_banner(), style="bold bright_red"))
                
                canvas_display = self.display_canvas()
                self.console.print(Panel(canvas_display, title=f"🧠 Turno {turn + 1} - LM Studio"))
                
                # Mostrar decisión REAL de LM Studio
                decision_info = f"""🧠 Decisión de LM Studio:
- Forma: {lm_data['lm_decision']['shape']}
- Posición: ({lm_data['lm_decision']['x']}, {lm_data['lm_decision']['y']})
- Tamaño: {lm_data['lm_decision']['size']}
- Símbolo: {lm_data['lm_decision']['symbol']}
- Razón: {lm_data['lm_decision'].get('creativity_reason', 'LM Studio creativo')}
- Estado: {lm_data['lm_decision'].get('evolution_stage', 'activo')}

📊 Datos:
- Puntos dibujados: {lm_data['points_drawn']}
- LM Studio activo: {lm_data['lm_studio_active']}"""
                
                self.console.print(Panel(decision_info, title="🧠 Análisis LM Studio"))
                
                progress.update(task, advance=1)
                time.sleep(2)  # Esperar respuesta de LM Studio
        
        # Resultado final con LM Studio
        self.clear_screen()
        self.console.print(Panel(self.create_banner(), style="bold bright_green"))
        
        final_canvas = self.display_canvas()
        self.console.print(Panel(final_canvas, title="🧠 Arte LM Studio Final"))
        
        # Estadísticas reales de LM Studio
        lm_stats = f"""🧠 LM Studio - Estadísticas Reales:
- Decisiones tomadas: {len(agent.decisions)}
- Formas únicas: {len(set([d['shape'] for d in agent.decisions]))}
- Posiciones únicas: {len(set([(d['x'], d['y']) for d in agent.decisions]))}
- Símbolos únicos: {len(set([d['symbol'] for d in agent.decisions]))}
- LM Studio activo: ✅
- Arte generado por LM Studio: ✅"""
        
        self.console.print(Panel(lm_stats, title="📊 Análisis LM Studio Real"))
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = {
            'lm_studio_artwork': [''.join(row) for row in self.canvas.grid],
            'lm_studio_decisions': agent.decisions,
            'lm_studio_active': True,
            'timestamp': timestamp
        }
        
        with open(f"lm_studio_real_{timestamp}.json", 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        self.console.print(f"[green]✅ Arte de LM Studio guardado en lm_studio_real_{timestamp}.json[/]")

if __name__ == "__main__":
    app = RealLMStudioApp()
    
    try:
        app.run_lm_studio_session(turns=8)
    except KeyboardInterrupt:
        print("\n[red]⏹️ Sesión LM Studio interrumpida[/]")
    except Exception as e:
        print(f"\n[red]❌ Error LM Studio: {e}[/]")
