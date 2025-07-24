#!/usr/bin/env python3
"""
MASTER ORGANIZER CON FIGURAS ASCII VISUALES
Ejecuta todos los sistemas y guarda arte ASCII completo
"""

import os
import json
import subprocess
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

class MasterVisualSystem:
    def __init__(self):
        self.console = Console()
        self.base_path = "/Users/carteaga/Projects/Agente_Dibuja/creaciones_lm_studio/artefinal"
        
    def run_visual_systems(self):
        self.console.print(Panel.fit(
            "🎭 [bold magenta]MASTER ORGANIZER - ARTE ASCII VISUAL[/]\n"
            "Ejecutando todos los sistemas con arte ASCII completo",
            border_style="magenta"
        ))
        
        results = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Ejecutar sistema genético visual
        self.console.print("\n🧬 [bold green]Ejecutando Genético Visual...[/]")
        try:
            genetic_path = "/Users/carteaga/Projects/Agente_Dibuja/creaciones_lm_studio/genetico/lm_studio_genetic_visual.py"
            subprocess.run(["python", genetic_path], check=True)
            results['genetic'] = {'status': 'success', 'visual': True}
            self.console.print("✅ Genético visual completado")
        except Exception as e:
            results['genetic'] = {'status': 'error', 'error': str(e)}
            self.console.print(f"❌ Error en genético: {e}")
        
        # Ejecutar sistema cuántico visual
        self.console.print("\n⚛️ [bold cyan]Ejecutando Cuántico Visual...[/]")
        try:
            quantum_path = "/Users/carteaga/Projects/Agente_Dibuja/creaciones_lm_studio/cuantico/lm_studio_quantum_visual.py"
            subprocess.run(["python", quantum_path], check=True)
            results['quantum'] = {'status': 'success', 'visual': True}
            self.console.print("✅ Cuántico visual completado")
        except Exception as e:
            results['quantum'] = {'status': 'error', 'error': str(e)}
            self.console.print(f"❌ Error en cuántico: {e}")
        
        # Ejecutar sistema diverso visual
        self.console.print("\n🎨 [bold yellow]Ejecutando Diversidad Visual...[/]")
        try:
            diverse_path = "/Users/carteaga/Projects/Agente_Dibuja/creaciones_lm_studio/diversidad/lm_studio_diverse_visual.py"
            subprocess.run(["python", diverse_path], check=True)
            results['diverse'] = {'status': 'success', 'visual': True}
            self.console.print("✅ Diversidad visual completada")
        except Exception as e:
            results['diverse'] = {'status': 'error', 'error': str(e)}
            self.console.print(f"❌ Error en diversidad: {e}")
        
        # Crear resumen visual
        summary = {
            'master_visual_session': {
                'timestamp': timestamp,
                'session_type': 'visual_ascii_complete',
                'systems_executed': results,
                'visual_artifacts': {
                    'genetic': 'lm_studio_genetic_visual.py',
                    'quantum': 'lm_studio_quantum_visual.py', 
                    'diverse': 'lm_studio_diverse_visual.py'
                },
                'folder': self.base_path,
                'visual_summary': True,
                'ascii_art_generated': True,
                'session_complete': True
            }
        }
        
        # Guardar resumen
        filepath = f"{self.base_path}/master_visual_{timestamp}.json"
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Mostrar tabla de resultados
        table = Table(title="📊 Resumen Visual Master")
        table.add_column("Sistema", style="cyan")
        table.add_column("Estado", style="green")
        table.add_column("Visual", style="yellow")
        
        for system, data in results.items():
            status = "✅ Éxito" if data['status'] == 'success' else "❌ Error"
            visual = "🎨 Arte ASCII" if data.get('visual') else "📊 Datos"
            table.add_row(system.title(), status, visual)
        
        self.console.print(table)
        self.console.print(f"\n[green]✅ Sesión visual master guardada en: {filepath}[/]")
        
        return filepath

if __name__ == "__main__":
    master = MasterVisualSystem()
    master.run_visual_systems()
