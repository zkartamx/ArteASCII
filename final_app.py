#!/usr/bin/env python3
"""
Agente Dibuja - Versión Final
Aplicación completa con interfaz de consola y arte ASCII
"""

import os
import sys
import time
from openai import OpenAI
from sync_agent import SyncDrawingAgent, SyncCanvas

class FinalAgentApp:
    def __init__(self):
        self.canvas = SyncCanvas(30, 15)
        self.client = None
        self.agent1 = None
        self.agent2 = None
        self.lm_studio_url = "http://localhost:1234/v1"
        
    def clear_screen(self):
        """Limpiar pantalla"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_banner(self):
        """Mostrar banner ASCII"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                    🎨 AGENTE DIBUJA                        ║
║              Arte ASCII Multi-Agente                        ║
║                    Versión Final                          ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def display_canvas(self, title="Canvas Actual"):
        """Mostrar canvas con título"""
        print(f"\n📋 {title}")
        print("─" * 32)
        for row in self.canvas.grid:
            print(''.join(row))
        print("─" * 32)
    
    def test_connection(self):
        """Probar conexión con LM Studio"""
        try:
            client = OpenAI(base_url=self.lm_studio_url, api_key="not-needed")
            
            # Test simple
            response = client.chat.completions.create(
                model="local-model",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1
            )
            
            self.client = client
            print("✅ LM Studio conectado exitosamente")
            return True
            
        except Exception as e:
            print(f"❌ Error conectando a LM Studio: {e}")
            print("\nVerifica que:")
            print("   • LM Studio esté ejecutándose")
            print("   • El modelo esté cargado")
            print("   • La URL sea: http://localhost:1234/v1")
            return False
    
    def create_agents(self, name1="Agente_Azul", name2="Agente_Rojo"):
        """Crear agentes"""
        if not self.client:
            print("❌ Primero conecta a LM Studio")
            return False
            
        symbols = ["█", "▓", "▒", "░", "▄", "▀", "▌", "▐", "•", "+"]
        self.agent1 = SyncDrawingAgent(name1, self.client, self.canvas, symbols)
        self.agent2 = SyncDrawingAgent(name2, self.client, self.canvas, symbols)
        
        print(f"✅ Agentes creados: {name1} y {name2}")
        return True
    
    def run_drawing_session(self, turns=20, delay=1.0):
        """Ejecutar sesión de dibujo completa"""
        if not self.agent1 or not self.agent2:
            print("❌ Crea agentes primero")
            return
        
        self.clear_screen()
        self.display_banner()
        
        agents = [self.agent1, self.agent2]
        agent_names = [self.agent1.name, self.agent2.name]
        
        print(f"\n🚀 Iniciando dibujo con {turns} turnos...")
        print(f"Agentes: {agent_names[0]} vs {agent_names[1]}")
        print(f"Delay: {delay} segundos")
        
        try:
            for turn in range(turns):
                agent = agents[turn % 2]
                current_agent = agent_names[turn % 2]
                
                # Hacer movimiento
                move = agent.make_move(turn)
                
                # Actualizar pantalla
                self.clear_screen()
                self.display_banner()
                
                print(f"\n🎯 Turno {turn + 1}/{turns}")
                print(f"🤖 Agente: {current_agent}")
                print(f"✏️  Símbolo: '{move['symbol']}'")
                print(f"📍 Posición: ({move['x']}, {move['y']})")
                print(f"💭 Razón: {move['reason']}")
                
                self.display_canvas()
                
                # Barra de progreso
                progress = (turn + 1) / turns * 100
                bar = "█" * int(progress / 5) + "░" * (20 - int(progress / 5))
                print(f"\n📊 Progreso: [{bar}] {progress:.1f}%")
                
                time.sleep(delay)
                
        except KeyboardInterrupt:
            print("\n\n⏹️ Dibujo interrumpido por el usuario")
            return
        except Exception as e:
            print(f"\n❌ Error durante el dibujo: {e}")
            return
        
        # Resultado final
        self.clear_screen()
        self.display_banner()
        
        print("\n🎨 ¡Dibujo completado exitosamente!")
        
        # Estadísticas
        patterns = self.canvas.analyze_patterns()
        print(f"\n📊 Estadísticas:")
        print(f"   • Canvas llenado: {patterns['filled_percentage']:.1f}%")
        print(f"   • Símbolos únicos: {patterns['unique_symbols']}")
        
        self.display_canvas("🎨 Arte Final")
    
    def save_artwork(self, filename="arte_ascii"):
        """Guardar arte en archivo"""
        try:
            with open(f"{filename}.txt", 'w', encoding='utf-8') as f:
                f.write("=== ARTE ASCII - AGENTE DIBUJA ===\n")
                f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 40 + "\n\n")
                
                for row in self.canvas.grid:
                    f.write(''.join(row) + '\n')
                    
                f.write("\n" + "=" * 40)
                
            print(f"✅ Arte guardado en {filename}.txt")
            return True
        except Exception as e:
            print(f"❌ Error guardando: {e}")
            return False
    
    def interactive_mode(self):
        """Modo interactivo completo"""
        self.clear_screen()
        
        print("🎨 AGENTE DIBUJA - MODO INTERACTIVO")
        print("=" * 50)
        
        # Paso 1: Conectar a LM Studio
        print("\n1. 🔗 Conectando a LM Studio...")
        if not self.test_connection():
            input("\nPresiona Enter para salir...")
            return
        
        # Paso 2: Crear agentes
        print("\n2. 🤖 Creando agentes...")
        name1 = input("Nombre del Agente 1 (default: Agente_Azul): ").strip() or "Agente_Azul"
        name2 = input("Nombre del Agente 2 (default: Agente_Rojo): ").strip() or "Agente_Rojo"
        
        if not self.create_agents(name1, name2):
            input("\nPresiona Enter para salir...")
            return
        
        # Paso 3: Configurar dibujo
        print("\n3. ⚙️ Configurando dibujo...")
        try:
            turns = int(input("Número de turnos (default: 20): ").strip() or "20")
            delay = float(input("Delay entre turnos (default: 1.0): ").strip() or "1.0")
        except ValueError:
            turns = 20
            delay = 1.0
            print("Usando valores por defecto")
        
        # Paso 4: Ejecutar dibujo
        print("\n4. 🚀 Ejecutando dibujo...")
        self.run_drawing_session(turns, delay)
        
        # Paso 5: Guardar resultado
        save = input("\n¿Guardar arte? (s/n): ").lower()
        if save == 's':
            filename = input("Nombre del archivo (default: arte_ascii): ").strip() or "arte_ascii"
            self.save_artwork(filename)
        
        print("\n👋 ¡Gracias por usar Agente Dibuja!")

if __name__ == "__main__":
    app = FinalAgentApp()
    
    try:
        app.interactive_mode()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
