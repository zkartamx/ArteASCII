#!/usr/bin/env python3
"""
Agente Dibuja - Versión Mejorada
Con interfaz enriquecida y características avanzadas
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
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.align import Align

class EnhancedApp:
    def __init__(self):
        self.console = Console()
        self.canvas = SyncCanvas(35, 18)
        self.client = None
        self.agent1 = None
        self.agent2 = None
        self.stats = {
            'turns': 0,
            'symbols_used': set(),
            'start_time': None,
            'patterns_analyzed': 0
        }
    
    def create_banner(self):
        """Crear banner ASCII mejorado"""
        banner = """
    █████████████████████████████████████████████████████████████
    █                                                           █
    █   🎨  AGENTE DIBUJA  -  ARTE ASCII MULTI-AGENTE  🎨     █
    █                                                           █
    █   Inteligencia Artificial + Creatividad + Colaboración   █
    █                                                           █
    █████████████████████████████████████████████████████████████
        """
        return banner
    
    def display_enhanced_canvas(self):
        """Mostrar canvas con estilo mejorado"""
        canvas_content = []
        for row in self.canvas.grid:
            # Añadir colores para símbolos diferentes
            colored_row = row.replace('█', '[bold blue]█[/]').replace('▓', '[bold red]▓[/]').replace('▒', '[bold yellow]▒[/]').replace('░', '[bold green]░[/]')
            canvas_content.append(colored_row)
        
        return '\n'.join(canvas_content)
    
    def create_stats_table(self):
        """Crear tabla de estadísticas"""
        table = Table(title="📊 Estadísticas del Dibujo")
        
        patterns = self.canvas.analyze_patterns()
        
        table.add_column("Métrica", style="cyan", no_wrap=True)
        table.add_column("Valor", style="magenta")
        
        table.add_row("Canvas llenado", f"{patterns['filled_percentage']:.1f}%")
        table.add_row("Símbolos únicos", str(patterns['unique_symbols']))
        table.add_row("Turnos completados", str(self.stats['turns']))
        table.add_row("Tiempo transcurrido", f"{time.time() - self.stats['start_time']:.1f}s")
        
        return table
    
    def enhanced_drawing_session(self, turns=25, delay=1.5):
        """Sesión de dibujo mejorada con UI rica"""
        self.stats['start_time'] = time.time()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            task = progress.add_task("[cyan]Iniciando dibujo...", total=turns)
            
            for turn in range(turns):
                agent = self.agent1 if turn % 2 == 0 else self.agent2
                agent_name = self.agent1.name if turn % 2 == 0 else self.agent2.name
                
                move = agent.make_move(turn)
                
                # Actualizar estadísticas
                self.stats['turns'] = turn + 1
                self.stats['symbols_used'].add(move['symbol'])
                
                # Actualizar progreso
                progress.update(task, description=f"[green]Turno {turn + 1}/{turns} - {agent_name}")
                
                # Mostrar canvas actualizado
                self.console.clear()
                self.console.print(Panel(self.create_banner(), style="bold blue"))
                
                # Canvas
                canvas_panel = Panel(
                    self.display_enhanced_canvas(),
                    title=f"🎨 Turno {turn + 1} - {agent_name}",
                    border_style="bright_yellow"
                )
                self.console.print(canvas_panel)
                
                # Información del movimiento
                info_panel = Panel(
                    f"✏️ Símbolo: '{move['symbol']}'\n"
                    f"📍 Posición: ({move['x']}, {move['y']})\n"
                    f"💭 Razón: {move['reason']}",
                    title="📋 Información del Movimiento",
                    border_style="bright_green"
                )
                self.console.print(info_panel)
                
                # Estadísticas
                self.console.print(self.create_stats_table())
                
                time.sleep(delay)
                progress.update(task, advance=1)
    
    def run_enhanced_mode(self):
        """Ejecutar versión mejorada completa"""
        self.console.clear()
        self.console.print(Panel(self.create_banner(), style="bold blue"))
        
        # Conectar a LM Studio
        self.console.print("[yellow]🔗 Conectando a LM Studio...[/]")
        try:
            self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
            self.console.print("[green]✅ LM Studio conectado exitosamente[/]")
        except Exception as e:
            self.console.print(f"[red]❌ Error: {e}[/]")
            return False
        
        # Crear agentes
        symbols = ["█", "▓", "▒", "░", "▄", "▀", "▌", "▐", "•", "+", "■", "◆"]
        self.agent1 = SyncDrawingAgent("🎨 Picasso", self.client, self.canvas, symbols)
        self.agent2 = SyncDrawingAgent("🖌️ Van_Gogh", self.client, self.canvas, symbols)
        
        # Configuración interactiva
        self.console.print("[cyan]⚙️ Configurando dibujo...[/]")
        
        # Sesión de dibujo mejorada
        self.enhanced_drawing_session(turns=30, delay=1.2)
        
        # Resultado final
        self.console.clear()
        self.console.print(Panel(self.create_banner(), style="bold green"))
        
        final_canvas = Panel(
            self.display_enhanced_canvas(),
            title="🎨 Arte Final - ¡Dibujo Completado!",
            border_style="bright_magenta"
        )
        self.console.print(final_canvas)
        
        # Guardar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"arte_mejorado_{timestamp}"
        
        with open(f"{filename}.txt", 'w', encoding='utf-8') as f:
            f.write(self.create_banner() + "\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            f.write(self.display_enhanced_canvas())
        
        self.console.print(f"[green]✅ Arte guardado en {filename}.txt[/]")
        
        return True

if __name__ == "__main__":
    app = EnhancedApp()
    
    try:
        app.run_enhanced_mode()
    except KeyboardInterrupt:
        print("\n[red]⏹️ Proceso interrumpido por el usuario[/]")
    except Exception as e:
        print(f"\n[red]❌ Error: {e}[/]")
