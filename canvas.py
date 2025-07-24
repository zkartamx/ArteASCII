from typing import List, Tuple, Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import random

class Canvas:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]
        self.console = Console()
        self.draw_history = []
    
    def draw_pixel(self, x: int, y: int, symbol: str, agent_name: str) -> bool:
        if 0 <= x < self.width and 0 <= y < self.height:
            old_value = self.grid[y][x]
            self.grid[y][x] = symbol
            self.draw_history.append({
                'agent': agent_name,
                'x': x,
                'y': y,
                'symbol': symbol,
                'old_value': old_value
            })
            return True
        return False
    
    def get_pixel(self, x: int, y: int) -> str:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return ' '
    
    def get_empty_positions(self) -> List[Tuple[int, int]]:
        empty = []
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == ' ':
                    empty.append((x, y))
        return empty
    
    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        neighbors = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbors.append((nx, ny))
        return neighbors
    
    def display(self, current_agent: Optional[str] = None):
        self.console.clear()
        
        # Crear el canvas visual
        canvas_lines = []
        for row in self.grid:
            line = ''.join(row)
            canvas_lines.append(line)
        
        canvas_content = '\n'.join(canvas_lines)
        
        # Panel principal
        title = f"🎨 Canvas ASCII - Turno de: {current_agent}" if current_agent else "🎨 Canvas ASCII"
        panel = Panel(
            canvas_content,
            title=title,
            subtitle=f"{self.width}x{self.height} - Historial: {len(self.draw_history)}",
            border_style="cyan"
        )
        
        self.console.print(panel)
        
        # Mostrar estadísticas
        if self.draw_history:
            last_5 = self.draw_history[-5:]
            self.console.print("\n[dim]Últimos movimientos:[/dim]")
            for move in last_5:
                self.console.print(f"  {move['agent']} dibujó '{move['symbol']}' en ({move['x']}, {move['y']})")
    
    def get_canvas_state(self) -> str:
        return '\n'.join([''.join(row) for row in self.grid])
    
    def analyze_patterns(self) -> dict:
        total_pixels = self.width * self.height
        filled_pixels = sum(1 for row in self.grid for cell in row if cell != ' ')
        empty_pixels = total_pixels - filled_pixels
        
        symbol_counts = {}
        for row in self.grid:
            for cell in row:
                if cell != ' ':
                    symbol_counts[cell] = symbol_counts.get(cell, 0) + 1
        
        return {
            'filled_percentage': (filled_pixels / total_pixels) * 100,
            'empty_percentage': (empty_pixels / total_pixels) * 100,
            'symbol_distribution': symbol_counts,
            'total_moves': len(self.draw_history)
        }
