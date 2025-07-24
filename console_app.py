#!/usr/bin/env python3
"""
Agente Dibuja - Versión Consola
Interfaz simple que funciona en la terminal sin problemas de navegador
"""

import os
import sys
import time
from openai import OpenAI
from canvas import Canvas
from agent import DrawingAgent
from config import Config

class ConsoleInterface:
    def __init__(self):
        self.config = Config()
        self.canvas = Canvas(30, 15)
        self.client = None
        self.agent1 = None
        self.agent2 = None
        self.running = False
        
    def clear_screen(self):
        """Limpiar pantalla"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self):
        """Mostrar encabezado"""
        print("=" * 60)
        print("🎨 AGENTE DIBUJA - ARTE ASCII MULTI-AGENTE")
        print("=" * 60)
    
    def display_canvas(self):
        """Mostrar canvas ASCII"""
        print("\n📋 Canvas Actual:")
        print("-" * 30)
        for row in self.canvas.grid:
            print(''.join(row))
        print("-" * 30)
    
    def connect_lm_studio(self, url):
        """Conectar a LM Studio"""
        try:
            self.client = OpenAI(base_url=url, api_key="not-needed")
            # Probar conexión
            self.client.chat.completions.create(
                model="local-model",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1
            )
            return True, "✅ LM Studio conectado exitosamente"
        except Exception as e:
            return False, f"❌ Error conectando a LM Studio: {e}"
    
    def create_agents(self, name1, name2):
        """Crear agentes"""
        if not self.client:
            return False, "❌ Primero debes conectar a LM Studio"
        
        symbols = ["█", "▓", "▒", "░", "▄", "▀", "▌", "▐"]
        self.agent1 = DrawingAgent(name1, self.client, self.canvas, symbols)
        self.agent2 = DrawingAgent(name2, self.client, self.canvas, symbols)
        return True, f"✅ Agentes creados: {name1} y {name2}"
    
    def start_drawing(self, turns, delay):
        """Iniciar proceso de dibujo"""
        if not self.agent1 or not self.agent2:
            return False, "❌ Primero crea los agentes"
        
        self.clear_screen()
        self.display_header()
        print(f"🚀 Iniciando dibujo con {turns} turnos...")
        
        agents = [self.agent1, self.agent2]
        idx = 0
        
        for turn in range(turns):
            agent = agents[idx]
            try:
                move = agent.make_move(turn)
                
                # Mostrar progreso
                self.clear_screen()
                self.display_header()
                print(f"\n🎯 Turno {turn + 1}/{turns}")
                print(f"🤖 Agente: {agent.name}")
                print(f"✏️  Símbolo: '{move['symbol']}'")
                print(f"📍 Posición: ({move['x']}, {move['y']})")
                
                self.display_canvas()
                
                # Barra de progreso simple
                progress = (turn + 1) / turns * 100
                bar = "█" * int(progress / 5) + "░" * (20 - int(progress / 5))
                print(f"\n📊 Progreso: [{bar}] {progress:.1f}%")
                
                time.sleep(delay)
                idx = (idx + 1) % 2
                
            except KeyboardInterrupt:
                print("\n⏹️ Proceso interrumpido por el usuario")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                break
        
        # Mostrar resultado final
        self.clear_screen()
        self.display_header()
        print("\n🎨 ¡Dibujo completado!")
        self.display_canvas()
        
        # Estadísticas
        patterns = self.canvas.analyze_patterns()
        print(f"\n📊 Estadísticas:")
        print(f"   • Canvas llenado: {patterns['filled_percentage']:.1f}%")
        print(f"   • Símbolos únicos: {len(set([cell for row in self.canvas.grid for cell in row if cell != ' ']))}")
        
        return True, "Proceso completado"
    
    def save_artwork(self, filename):
        """Guardar arte en archivo"""
        try:
            with open(f"{filename}.txt", 'w') as f:
                f.write("=== ARTE ASCII - AGENTE DIBUJA ===\n\n")
                for row in self.canvas.grid:
                    f.write(''.join(row) + '\n')
            return True, f"✅ Arte guardado en {filename}.txt"
        except Exception as e:
            return False, f"❌ Error guardando: {e}"
    
    def run(self):
        """Ejecutar interfaz de consola"""
        self.clear_screen()
        
        while True:
            self.display_header()
            print("\n📋 Menú Principal:")
            print("   1. 🔗 Conectar a LM Studio")
            print("   2. 🤖 Crear Agentes")
            print("   3. 🚀 Iniciar Dibujo")
            print("   4. 🔄 Resetear Canvas")
            print("   5. 💾 Guardar Arte")
            print("   6. ❌ Salir")
            
            choice = input("\nSelecciona una opción (1-6): ").strip()
            
            if choice == "1":
                url = input("URL de LM Studio (default: http://localhost:1234/v1): ").strip()
                if not url:
                    url = "http://localhost:1234/v1"
                success, msg = self.connect_lm_studio(url)
                print(f"\n{msg}")
                input("\nPresiona Enter para continuar...")
                
            elif choice == "2":
                name1 = input("Nombre del Agente 1 (default: Agente_Azul): ").strip() or "Agente_Azul"
                name2 = input("Nombre del Agente 2 (default: Agente_Rojo): ").strip() or "Agente_Rojo"
                success, msg = self.create_agents(name1, name2)
                print(f"\n{msg}")
                input("\nPresiona Enter para continuar...")
                
            elif choice == "3":
                try:
                    turns = int(input("Número de turnos (default: 20): ").strip() or "20")
                    delay = float(input("Delay entre turnos en segundos (default: 1.0): ").strip() or "1.0")
                    success, msg = self.start_drawing(turns, delay)
                    print(f"\n{msg}")
                    input("\nPresiona Enter para continuar...")
                except ValueError:
                    print("❌ Por favor ingresa números válidos")
                    input("\nPresiona Enter para continuar...")
                    
            elif choice == "4":
                self.reset_canvas()
                print("\n✅ Canvas reseteado")
                self.display_canvas()
                input("\nPresiona Enter para continuar...")
                
            elif choice == "5":
                filename = input("Nombre del archivo (default: mi_arte): ").strip() or "mi_arte"
                success, msg = self.save_artwork(filename)
                print(f"\n{msg}")
                input("\nPresiona Enter para continuar...")
                
            elif choice == "6":
                print("\n👋 ¡Hasta luego!")
                break
                
            else:
                print("❌ Opción no válida")
                input("\nPresiona Enter para continuar...")
            
            self.clear_screen()

if __name__ == "__main__":
    app = ConsoleInterface()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
        sys.exit(0)
