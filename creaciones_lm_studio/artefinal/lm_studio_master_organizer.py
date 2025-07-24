#!/usr/bin/env python3
"""
MASTER ORGANIZADOR LM STUDIO
Gestiona todas las carpetas de creaciones
"""

import os
import json
import subprocess
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

class MasterLMStudioOrganizer:
    def __init__(self):
        self.console = Console()
        self.base_path = "/Users/carteaga/Projects/Agente_Dibuja/creaciones_lm_studio"
        self.folders = {
            'genetico': f"{self.base_path}/genetico",
            'cuantico': f"{self.base_path}/cuantico",
            'diversidad': f"{self.base_path}/diversidad",
            'artefinal': f"{self.base_path}/artefinal"
        }
        
    def show_folder_structure(self):
        table = Table(title="📁 Estructura de Carpetas LM Studio")
        table.add_column("Sistema", style="cyan")
        table.add_column("Carpeta", style="magenta")
        table.add_column("Archivos", style="green")
        
        for system, path in self.folders.items():
            files = len([f for f in os.listdir(path) if f.endswith('.json')])
            table.add_row(system.capitalize(), path, str(files))
        
        self.console.print(table)
    
    def run_all_systems(self):
        self.console.print(Panel("""
🚀 [bold bright_blue]MASTER ORGANIZADOR LM STUDIO[/]
Ejecutando todos los sistemas en sus carpetas
        """, style="bold bright_blue"))
        
        results = {}
        
        # Ejecutar genetico
        try:
            result = subprocess.run([
                'python', f"{self.folders['genetico']}/lm_studio_genetic_organizer.py"
            ], capture_output=True, text=True)
            results['genetico'] = '✅ Completado'
            self.console.print("[green]✅ Genético ejecutado[/]")
        except Exception as e:
            results['genetico'] = f'❌ Error: {e}'
        
        # Ejecutar cuantico
        try:
            result = subprocess.run([
                'python', f"{self.folders['cuantico']}/lm_studio_quantum_organizer.py"
            ], capture_output=True, text=True)
            results['cuantico'] = '✅ Completado'
            self.console.print("[cyan]✅ Cuántico ejecutado[/]")
        except Exception as e:
            results['cuantico'] = f'❌ Error: {e}'
        
        # Ejecutar diversidad
        try:
            result = subprocess.run([
                'python', f"{self.folders['diversidad']}/lm_studio_diverse_organizer.py"
            ], capture_output=True, text=True)
            results['diversidad'] = '✅ Completado'
            self.console.print("[yellow]✅ Diversidad ejecutada[/]")
        except Exception as e:
            results['diversidad'] = f'❌ Error: {e}'
        
        # Guardar resumen
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary = {
            'lm_studio_master_session': {
                'results': results,
                'folders': self.folders,
                'timestamp': timestamp,
                'session_type': 'lm_studio_complete'
            }
        }
        
        filepath = f"{self.folders['artefinal']}/master_session_{timestamp}.json"
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2)
        
        self.console.print(f"\n[green]✅ Sesión master guardada: {filepath}[/]")
        self.show_folder_structure()

if __name__ == "__main__":
    master = MasterLMStudioOrganizer()
    master.run_all_systems()
