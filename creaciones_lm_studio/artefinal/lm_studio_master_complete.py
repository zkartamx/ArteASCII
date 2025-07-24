#!/usr/bin/env python3
"""
MASTER COMPLETO CON ARTE ASCII REAL
Ejecuta todos los sistemas y guarda arte ASCII exactamente como los archivos externos
"""

import os
import json
import subprocess
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

class MasterCompleteSystem:
    def __init__(self):
        self.console = Console()
        self.base_path = "/Users/carteaga/Projects/Agente_Dibuja/creaciones_lm_studio/artefinal"
        
    def run_complete_systems(self):
        self.console.print(Panel.fit(
            "🎭 [bold magenta]MASTER COMPLETO - ARTE ASCII REAL[/]\n"
            "Ejecutando todos los sistemas con arte ASCII completo",
            border_style="magenta"
        ))
        
        results = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Ejecutar sistema genético completo
        self.console.print("\n🧬 [bold green]Ejecutando Genético Completo...[/]")
        try:
            genetic_path = "/Users/carteaga/Projects/Agente_Dibuja/creaciones_lm_studio/genetico/lm_studio_genetic_complete.py"
            subprocess.run(["python", genetic_path], check=True)
            results['genetic'] = {'status': 'success', 'complete': True}
            self.console.print("✅ Genético completo ejecutado")
        except Exception as e:
            results['genetic'] = {'status': 'error', 'error': str(e)}
            self.console.print(f"❌ Error en genético: {e}")
        
        # Ejecutar sistema cuántico completo
        self.console.print("\n⚛️ [bold cyan]Ejecutando Cuántico Completo...[/]")
        try:
            quantum_path = "/Users/carteaga/Projects/Agente_Dibuja/creaciones_lm_studio/cuantico/lm_studio_quantum_complete.py"
            subprocess.run(["python", quantum_path], check=True)
            results['quantum'] = {'status': 'success', 'complete': True}
            self.console.print("✅ Cuántico completo ejecutado")
        except Exception as e:
            results['quantum'] = {'status': 'error', 'error': str(e)}
            self.console.print(f"❌ Error en cuántico: {e}")
        
        # Ejecutar sistema diverso completo
        self.console.print("\n🎨 [bold yellow]Ejecutando Diversidad Completa...[/]")
        try:
            diverse_path = "/Users/carteaga/Projects/Agente_Dibuja/creaciones_lm_studio/diversidad/lm_studio_diverse_complete.py"
            subprocess.run(["python", diverse_path], check=True)
            results['diverse'] = {'status': 'success', 'complete': True}
            self.console.print("✅ Diversidad completa ejecutada")
        except Exception as e:
            results['diverse'] = {'status': 'error', 'error': str(e)}
            self.console.print(f"❌ Error en diversidad: {e}")
        
        # Crear resumen completo
        summary = {
            'lm_studio_master_complete': {
                'timestamp': timestamp,
                'session_type': 'complete_ascii_artwork',
                'systems_executed': results,
                'complete_systems': {
                    'genetic': 'lm_studio_genetic_complete.py',
                    'quantum': 'lm_studio_quantum_complete.py',
                    'diverse': 'lm_studio_diverse_complete.py'
                },
                'folder': self.base_path,
                'ascii_art_complete': True,
                'visual_artwork': True,
                'session_complete': True,
                'format': 'exactly_like_external_files'
            }
        }
        
        # Guardar resumen completo
        filepath = f"{self.base_path}/master_complete_{timestamp}.json"
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Mostrar tabla de resultados
        table = Table(title="📊 Resumen Master Completo")
        table.add_column("Sistema", style="cyan")
        table.add_column("Estado", style="green")
        table.add_column("Arte ASCII", style="yellow")
        
        for system, data in results.items():
            status = "✅ Completo" if data['status'] == 'success' else "❌ Error"
            art = "🎨 Figuras incluidas" if data['status'] == 'success' else "📊 Solo datos"
            table.add_row(system.title(), status, art)
        
        self.console.print(table)
        self.console.print(f"\n[green]✅ Sesión master completa guardada en: {filepath}[/]")
        
        return filepath

if __name__ == "__main__":
    master = MasterCompleteSystem()
    master.run_complete_systems()
