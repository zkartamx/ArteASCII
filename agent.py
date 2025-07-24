from typing import List, Tuple, Dict, Any
import openai
from openai import OpenAI
import random
import json
from canvas import Canvas
from config import Config

class DrawingAgent:
    def __init__(self, name: str, client: OpenAI, canvas: Canvas, symbols: List[str]):
        self.name = name
        self.client = client
        self.canvas = canvas
        self.symbols = symbols
        self.personal_style = self._develop_style()
        self.memory = []
    
    def _develop_style(self) -> Dict[str, Any]:
        styles = [
            {"approach": "minimalista", "preference": "bordes", "density": "baja"},
            {"approach": "expresivo", "preference": "centro", "density": "alta"},
            {"approach": "geométrico", "preference": "patrones", "density": "media"},
            {"approach": "orgánico", "preference": "flujo", "density": "media"}
        ]
        return random.choice(styles)
    
    async def make_move(self, turn_number: int) -> Dict[str, Any]:
        """El agente decide su próximo movimiento usando LM Studio"""
        
        # Preparar contexto para el modelo
        context = self._prepare_context(turn_number)
        
        try:
            response = self.client.chat.completions.create(
                model="local-model",
                messages=[
                    {
                        "role": "system",
                        "content": f"Eres {self.name}, un artista ASCII que dibuja en un canvas compartido. "
                                  f"Tu estilo es {self.personal_style['approach']} y prefieres {self.personal_style['preference']}. "
                                  f"Responde SOLO con JSON válido."
                    },
                    {
                        "role": "user",
                        "content": context
                    }
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            decision_text = response.choices[0].message.content
            decision = self._parse_decision(decision_text)
            
            # Validar y ejecutar la decisión
            if self._validate_move(decision):
                success = self.canvas.draw_pixel(
                    decision['x'], 
                    decision['y'], 
                    decision['symbol'], 
                    self.name
                )
                
                if success:
                    self.memory.append(decision)
                    return decision
            
            # Fallback si la decisión es inválida
            return self._make_random_move()
            
        except Exception as e:
            print(f"Error en {self.name}: {e}")
            return self._make_random_move()
    
    def _prepare_context(self, turn_number: int) -> str:
        canvas_state = self.canvas.get_canvas_state()
        empty_positions = self.canvas.get_empty_positions()
        
        # Análisis simple del estado actual
        patterns = self.canvas.analyze_patterns()
        
        context = f"""
Canvas actual:
{canvas_state}

Turno: {turn_number}
Posiciones vacías: {len(empty_positions)}
Estado del canvas:
- Llenado: {patterns['filled_percentage']:.1f}%
- Símbolos usados: {patterns['symbol_distribution']}

Como {self.name} con estilo {self.personal_style['approach']}, decide:
1. Coordenadas (x, y) donde dibujar (0-{self.canvas.width-1}, 0-{self.canvas.height-1})
2. Símbolo ASCII para usar
3. Breve justificación

Responde EXACTAMENTE con este formato JSON:
{{
    "x": número,
    "y": número,
    "symbol": "carácter",
    "reason": "tu justificación"
}}
"""
        return context
    
    def _parse_decision(self, response_text: str) -> Dict[str, Any]:
        try:
            # Limpiar el texto para extraer JSON válido
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = response_text[start:end]
                return json.loads(json_str)
        except:
            pass
        
        return self._make_random_move()
    
    def _validate_move(self, decision: Dict[str, Any]) -> bool:
        if not isinstance(decision, dict):
            return False
        
        required_keys = ['x', 'y', 'symbol', 'reason']
        if not all(key in decision for key in required_keys):
            return False
        
        x, y = decision['x'], decision['y']
        symbol = decision['symbol']
        
        # Validar coordenadas
        if not (0 <= x < self.canvas.width and 0 <= y < self.canvas.height):
            return False
        
        # Validar símbolo
        if not isinstance(symbol, str) or len(symbol) != 1:
            return False
        
        # No dibujar sobre posiciones ya ocupadas (opcional - podrías cambiar esto)
        if self.canvas.get_pixel(x, y) != ' ':
            return False
        
        return True
    
    def _make_random_move(self) -> Dict[str, Any]:
        empty_positions = self.canvas.get_empty_positions()
        if not empty_positions:
            return {"x": 0, "y": 0, "symbol": "?", "reason": "sin espacio"}
        
        x, y = random.choice(empty_positions)
        symbol = random.choice(self.symbols)
        
        return {
            "x": x,
            "y": y,
            "symbol": symbol,
            "reason": "movimiento aleatorio por fallback"
        }
    
    def get_stats(self) -> Dict[str, Any]:
        moves = [m for m in self.canvas.draw_history if m['agent'] == self.name]
        return {
            "name": self.name,
            "total_moves": len(moves),
            "style": self.personal_style,
            "memory_size": len(self.memory)
        }
