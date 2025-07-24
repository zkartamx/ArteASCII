#!/usr/bin/env python3
"""
Agente Dibuja - Versión Mejorada y Funcional
Con interfaz enriquecida usando Rich
"""

import os
import sys
import time
import random
from datetime import datetime
from openai import OpenAI
from sync_agent import SyncDrawingAgent, SyncCanvas
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from rich.live import Live

class WorkingEnhancedApp:
    def __init__(self):
        self.console = Console()
        self.canvas = SyncCanvas(30, 15)
        self.client = None
        self.agent1 = None
        self.agent2 = None
        
    def clear_screen(self):
        """Limpiar pantalla"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def create_banner(self):
        """Crear banner simple"""
        return """
╔══════════════════════════════════════════════════════════════╗
║                    🎨 AGENTE DIBUJA                        ║
║              Arte ASCII Multi-Agente                        ║
║                    Versión Mejorada                       ║
╚══════════════════════════════════════════════════════════════╝
        """
    
    def display_enhanced_canvas(self):
        """Mostrar canvas con colores"""
        lines = []
        for row in self.canvas.grid:
            # Crear texto con colores para diferentes símbolos
            colored_line = ""
            for char in row:
                if char == '█':
                    colored_line += '[bold blue]█[/]'
                elif char == '▓':
                    colored_line += '[bold red]▓[/]'
                elif char == '▒':
                    colored_line += '[bold yellow]▒[/]'
                elif char == '░':
                    colored_line += '[bold green]░[/]'
                elif char != ' ':
                    colored_line += f'[bold cyan]{char}[/]'
                else:
                    colored_line += ' '
            lines.append(colored_line)
        return '\n'.join(lines)
    
    def create_stats_table(self):
        """Crear tabla de estadísticas"""
        table = Table(title="📊 Estadísticas")
        
        patterns = self.canvas.analyze_patterns()
        
        table.add_column("Métrica", style="cyan")
        table.add_column("Valor", style="magenta")
        
        table.add_row("Canvas llenado", f"{patterns['filled_percentage']:.1f}%")
        table.add_row("Símbolos únicos", str(patterns['unique_symbols']))
        
        return table
    
    def enhanced_drawing_session(self, turns=25, delay=1.0):
        """Sesión de dibujo mejorada"""
        self.clear_screen()
        
        # Mostrar banner
        banner = self.create_banner()
        self.console.print(Panel(banner, style="bold blue"))
        
        # Información de inicio
        self.console.print(f"[yellow]🚀 Iniciando dibujo con {turns} turnos...[/]")
        self.console.print(f"[cyan]Agentes: {self.agent1.name} vs {self.agent2.name}[/]")
        
        for turn in range(turns):
            agent = self.agent1 if turn % 2 == 0 else self.agent2
            agent_name = self.agent1.name if turn % 2 == 0 else self.agent2.name
            
            move = agent.make_move(turn)
            
            self.clear_screen()
            
            # Mostrar información actualizada
            self.console.print(Panel(self.create_banner(), style="bold blue"))
            
            # Canvas
            canvas_display = self.display_enhanced_canvas()
            self.console.print(Panel(canvas_display, title=f"🎨 Turno {turn + 1} - {agent_name}"))
            
            # Información del movimiento
            info_text = f"✏️ Símbolo: '{move['symbol']}'\n📍 Posición: ({move['x']}, {move['y']})\n💭 Razón: {move['reason']}"
            self.console.print(Panel(info_text, title="📋 Información"))
            
            # Barra de progreso simple
            progress = (turn + 1) / turns * 100
            bar = "█" * int(progress / 4) + "░" * (25 - int(progress / 4))
            self.console.print(f"📊 Progreso: [{bar}] {progress:.1f}%")
            
            time.sleep(delay)
    
    def run_working_enhanced(self):
        """Ejecutar versión mejorada funcional"""
        self.clear_screen()
        
        # Conectar a LM Studio
        self.console.print("[yellow]🔗 Conectando a LM Studio...[/]")
        try:
            self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
            self.console.print("[green]✅ LM Studio conectado exitosamente[/]")
        except Exception as e:
            self.console.print(f"[red]❌ Error: {e}[/]")
            return False
        
        # Crear agentes con nombres creativos
        symbols = ["█", "▓", "▒", "░", "▄", "▀", "▌", "▐", "•", "+", "■", "◆"]
        self.agent1 = SyncDrawingAgent("🎨 Picasso", self.client, self.canvas, symbols)
        self.agent2 = SyncDrawingAgent("🖌️ Van_Gogh", self.client, self.canvas, symbols)
        
        # Configuración interactiva
        self.console.print("[cyan]⚙️ Configurando dibujo...[/]")
        
        # Ejecutar sesión mejorada
        self.enhanced_drawing_session(turns=20, delay=1.0)
        
        # Resultado final
        self.clear_screen()
        self.console.print(Panel(self.create_banner(), style="bold green"))
        
        # Canvas final
        final_canvas = self.display_enhanced_canvas()
        self.console.print(Panel(final_canvas, title="🎨 ¡Arte Final Completado!"))
        
        # Estadísticas
        patterns = self.canvas.analyze_patterns()
        stats_table = self.create_stats_table()
        self.console.print(stats_table)
        
        # Guardar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"arte_enhanced_{timestamp}"
        
        with open(f"{filename}.txt", 'w', encoding='utf-8') as f:
            f.write("=== ARTE ASCII MEJORADO ===\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            f.write('\n'.join([''.join(row) for row in self.canvas.grid]))
        
        self.console.print(f"[green]✅ Arte guardado en {filename}.txt[/]")
        
        return True

if __name__ == "__main__":
    app = WorkingEnhancedApp()
    
    try:
        app.run_working_enhanced()
    except KeyboardInterrupt:
        print("\n[red]⏹️ Proceso interrumpido[/]")
    except Exception as e:
        print(f"\n[red]❌ Error: {e}[/]")
