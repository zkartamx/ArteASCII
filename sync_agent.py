#!/usr/bin/env python3
"""
Agente síncrono que funciona correctamente con LM Studio
"""

import random
import json
import re
from typing import List, Dict, Any
from openai import OpenAI
from canvas import Canvas

class SyncDrawingAgent:
    def __init__(self, name: str, client: OpenAI, canvas: Canvas, symbols: List[str]):
        self.name = name
        self.client = client
        self.canvas = canvas
        self.symbols = symbols
        self.personal_style = self._develop_style()
        self.memory = []
    
    def _develop_style(self) -> Dict[str, Any]:
        """Desarrollar estilo personal del agente"""
        styles = [
            {"approach": "minimalista", "preference": "bordes", "density": "baja"},
            {"approach": "expresivo", "preference": "centro", "density": "alta"},
            {"approach": "geométrico", "preference": "patrones", "density": "media"},
            {"approach": "orgánico", "preference": "flujo", "density": "media"}
        ]
        return random.choice(styles)
    
    def _prepare_context(self, turn_number: int) -> str:
        """Preparar contexto para el modelo"""
        canvas_str = self.canvas.display()
        empty_positions = len(self.canvas.get_empty_positions())
        filled_positions = (self.canvas.width * self.canvas.height) - empty_positions
        
        context = f"""
Turno actual: {turn_number}
Canvas actual (20x10):
{canvas_str}

Estadísticas:
- Posiciones vacías: {empty_positions}
- Posiciones llenas: {filled_positions}
- Símbolos disponibles: {', '.join(self.symbols)}

Tu tarea: Decidir dónde dibujar y qué símbolo usar.
Responde con un JSON válido en este formato exacto:
{{"x": número, "y": número, "symbol": "símbolo", "reason": "breve explicación"}}

Consideraciones:
- Coordenadas válidas: x entre 0 y {self.canvas.width-1}, y entre 0 y {self.canvas.height-1}
- Solo usa símbolos de la lista: {', '.join(self.symbols)}
- Evita posiciones ya ocupadas
- {self.personal_style['approach']} estilo, prefieres {self.personal_style['preference']}
"""
        return context
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Parsear respuesta JSON del modelo"""
        try:
            # Buscar JSON en la respuesta
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                parsed = json.loads(json_str)
                
                # Validar y ajustar valores
                x = max(0, min(int(parsed.get('x', 0)), self.canvas.width - 1))
                y = max(0, min(int(parsed.get('y', 0)), self.canvas.height - 1))
                symbol = parsed.get('symbol', self.symbols[0])
                
                # Asegurar que el símbolo esté en la lista
                if symbol not in self.symbols:
                    symbol = random.choice(self.symbols)
                
                return {
                    "x": x,
                    "y": y,
                    "symbol": symbol,
                    "reason": parsed.get('reason', 'decisión artística')
                }
            else:
                # Fallback: movimiento aleatorio válido
                empty_positions = self.canvas.get_empty_positions()
                if empty_positions:
                    x, y = random.choice(empty_positions)
                    return {
                        "x": x,
                        "y": y,
                        "symbol": random.choice(self.symbols),
                        "reason": "movimiento aleatorio por falta de JSON válido"
                    }
                else:
                    return {
                        "x": random.randint(0, self.canvas.width - 1),
                        "y": random.randint(0, self.canvas.height - 1),
                        "symbol": random.choice(self.symbols),
                        "reason": "canvas lleno - movimiento forzado"
                    }
                    
        except Exception as e:
            print(f"Error parseando JSON: {e}")
            return self._get_fallback_move()
    
    def _get_fallback_move(self) -> Dict[str, Any]:
        """Movimiento de respaldo cuando hay error"""
        empty_positions = self.canvas.get_empty_positions()
        if empty_positions:
            x, y = random.choice(empty_positions)
        else:
            x = random.randint(0, self.canvas.width - 1)
            y = random.randint(0, self.canvas.height - 1)
        
        return {
            "x": x,
            "y": y,
            "symbol": random.choice(self.symbols),
            "reason": "movimiento de respaldo"
        }
    
    def make_move(self, turn_number: int) -> Dict[str, Any]:
        """Hacer un movimiento (versión síncrona)"""
        context = self._prepare_context(turn_number)
        
        try:
            response = self.client.chat.completions.create(
                model="local-model",
                messages=[
                    {
                        "role": "system",
                        "content": f"Eres {self.name}, un artista ASCII. Responde SOLO con JSON válido."
                    },
                    {
                        "role": "user",
                        "content": context
                    }
                ],
                temperature=0.7,
                max_tokens=100
            )
            
            response_text = response.choices[0].message.content
            move = self._parse_json_response(response_text)
            
            # Verificar que la posición esté vacía
            if self.canvas.grid[move['y']][move['x']] != ' ':
                empty_positions = self.canvas.get_empty_positions()
                if empty_positions:
                    move['x'], move['y'] = random.choice(empty_positions)
                    move['reason'] = "posición ocupada - ajustada"
            
            # Dibujar en el canvas
            self.canvas.draw_pixel(move['x'], move['y'], move['symbol'])
            
            return move
            
        except Exception as e:
            print(f"Error con LM Studio: {e}")
            return self._get_fallback_move()

class SyncCanvas:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    def draw_pixel(self, x: int, y: int, symbol: str):
        """Dibujar un pixel en el canvas"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = symbol
    
    def get_empty_positions(self):
        """Obtener posiciones vacías"""
        empty = []
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == ' ':
                    empty.append((x, y))
        return empty
    
    def display(self):
        """Mostrar canvas"""
        return '\n'.join([''.join(row) for row in self.grid])
    
    def analyze_patterns(self):
        """Análisis simple del canvas"""
        total_cells = self.width * self.height
        filled_cells = sum(1 for row in self.grid for cell in row if cell != ' ')
        
        return {
            'filled_percentage': (filled_cells / total_cells) * 100,
            'unique_symbols': len(set(cell for row in self.grid for cell in row if cell != ' '))
        }

# Función principal para pruebas
if __name__ == "__main__":
    import time
    
    print("🔍 PRUEBA DE AGENTE SÍNCRONO")
    print("=" * 40)
    
    # Verificar LM Studio
    try:
        client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
        
        # Test de conexión
        response = client.chat.completions.create(
            model="local-model",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=1
        )
        print("✅ LM Studio conectado exitosamente")
        
        # Crear canvas y agentes
        canvas = SyncCanvas(15, 8)
        symbols = ["█", "▓", "▒", "░"]
        agent1 = SyncDrawingAgent("Azul", client, canvas, symbols)
        agent2 = SyncDrawingAgent("Rojo", client, canvas, symbols)
        
        print("\n🚀 Iniciando dibujo...")
        
        for turn in range(6):
            agent = agent1 if turn % 2 == 0 else agent2
            
            move = agent.make_move(turn)
            
            print(f"\nTurno {turn + 1}")
            print(f"Agente: {agent.name}")
            print(f"Movimiento: {move}")
            print()
            
            # Mostrar canvas
            for row in canvas.grid:
                print(''.join(row))
            
            time.sleep(0.5)
        
        print("\n✅ Demo completada!")
        print(f"Canvas final:\n{canvas.display()}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nVerifica que:")
        print("   • LM Studio esté ejecutándose")
        print("   • El modelo esté cargado")
        print("   • La URL sea correcta: http://localhost:1234/v1")
