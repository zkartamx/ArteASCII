#!/usr/bin/env python3
"""
Agente Dibuja - Versión Debug
Con logging detallado para verificar conexión con LM Studio
"""

import os
import sys
import time
import requests
from openai import OpenAI
from canvas import Canvas
from agent import DrawingAgent

class DebugApp:
    def __init__(self):
        self.canvas = Canvas(20, 10)  # Canvas más pequeño para pruebas
        self.client = None
        self.agent1 = None
        self.agent2 = None
        self.lm_studio_url = "http://localhost:1234/v1"
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def test_lm_studio_connection(self):
        """Probar conexión con LM Studio"""
        print("🔍 Probando conexión con LM Studio...")
        
        try:
            # Test 1: Verificar que el servidor responda
            response = requests.get(f"{self.lm_studio_url}/models", timeout=5)
            if response.status_code == 200:
                print("✅ Servidor LM Studio está activo")
                models = response.json()
                print(f"📋 Modelos disponibles: {len(models.get('data', []))}")
                for model in models.get('data', []):
                    print(f"   • {model.get('id', 'unknown')}")
            else:
                print(f"❌ Error HTTP: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            print("❌ No se puede conectar a LM Studio")
            print("   • Verifica que LM Studio esté ejecutándose")
            print("   • Verifica que esté en http://localhost:1234")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
            
        return True
    
    def test_openai_client(self):
        """Probar cliente OpenAI"""
        print("\n🔍 Probando cliente OpenAI...")
        
        try:
            client = OpenAI(base_url=self.lm_studio_url, api_key="not-needed")
            
            # Hacer una prueba simple
            response = client.chat.completions.create(
                model="local-model",  # Usa el modelo por defecto
                messages=[{"role": "user", "content": "Hola, ¿funciona?"}],
                max_tokens=10,
                temperature=0.7
            )
            
            print("✅ Cliente OpenAI funciona correctamente")
            print(f"📤 Respuesta: {response.choices[0].message.content.strip()}")
            return client
            
        except Exception as e:
            print(f"❌ Error con cliente OpenAI: {e}")
            return None
    
    def create_test_agents(self):
        """Crear agentes de prueba"""
        print("\n🔍 Creando agentes de prueba...")
        
        client = self.test_openai_client()
        if not client:
            return False
            
        symbols = ["█", "▓", "▒"]
        self.agent1 = DrawingAgent("Test_Azul", client, self.canvas, symbols)
        self.agent2 = DrawingAgent("Test_Rojo", client, self.canvas, symbols)
        
        print("✅ Agentes creados exitosamente")
        return True
    
    def test_agent_move(self):
        """Probar que un agente haga un movimiento"""
        print("\n🔍 Probando movimiento de agente...")
        
        if not self.agent1:
            print("❌ No hay agentes creados")
            return False
            
        try:
            move = self.agent1.make_move(0)
            print("✅ Agente respondió correctamente")
            print(f"📤 Movimiento: {move}")
            return True
        except Exception as e:
            print(f"❌ Error en movimiento: {e}")
            return False
    
    def simple_drawing_demo(self):
        """Demostración simple de dibujo"""
        self.clear_screen()
        print("🎨 Demostración de dibujo ASCII")
        print("=" * 40)
        
        # Verificar conexión
        if not self.test_lm_studio_connection():
            return False
            
        # Crear cliente y agentes
        client = self.test_openai_client()
        if not client:
            return False
            
        symbols = ["█", "▓", "▒", "░"]
        agent1 = DrawingAgent("Demo1", client, self.canvas, symbols)
        agent2 = DrawingAgent("Demo2", client, self.canvas, symbols)
        
        print("\n🚀 Iniciando dibujo simple...")
        
        for turn in range(8):  # Solo 8 turnos para demo
            agent = agent1 if turn % 2 == 0 else agent2
            
            try:
                move = agent.make_move(turn)
                
                # Mostrar canvas actualizado
                self.clear_screen()
                print(f"Turno {turn + 1}/8")
                print(f"Agente: {agent.name}")
                print(f"Símbolo: '{move['symbol']}'")
                print()
                
                # Mostrar canvas
                for row in self.canvas.grid:
                    print(''.join(row))
                
                time.sleep(1)
                
            except Exception as e:
                print(f"Error en turno {turn + 1}: {e}")
                break
        
        print("\n✅ Demo completada!")
        return True
    
    def run_debug_session(self):
        """Ejecutar sesión de debug completa"""
        self.clear_screen()
        print("🔧 DEBUG DE AGENTE DIBUJA")
        print("=" * 50)
        
        print("\n1. Verificando conexión con LM Studio...")
        if not self.test_lm_studio_connection():
            return False
            
        print("\n2. Verificando cliente OpenAI...")
        client = self.test_openai_client()
        if not client:
            return False
            
        print("\n3. Creando agentes...")
        if not self.create_test_agents():
            return False
            
        print("\n4. Probando movimiento...")
        if not self.test_agent_move():
            return False
            
        print("\n5. Ejecutando demo...")
        self.simple_drawing_demo()
        
        return True
    
    def interactive_mode(self):
        """Modo interactivo simple"""
        self.clear_screen()
        
        print("🎨 AGENTE DIBUJA - MODO INTERACTIVO")
        print("=" * 40)
        
        # Verificar conexión
        if not self.test_lm_studio_connection():
            return False
            
        client = self.test_openai_client()
        if not client:
            return False
            
        # Crear agentes
        agent1_name = input("Nombre del Agente 1 (default: Agente_Azul): ") or "Agente_Azul"
        agent2_name = input("Nombre del Agente 2 (default: Agente_Rojo): ") or "Agente_Rojo"
        
        symbols = ["█", "▓", "▒", "░", "▄", "▀"]
        agent1 = DrawingAgent(agent1_name, client, self.canvas, symbols)
        agent2 = DrawingAgent(agent2_name, client, self.canvas, symbols)
        
        turns = int(input("Número de turnos (default: 10): ") or "10")
        delay = float(input("Delay entre turnos (default: 1.0): ") or "1.0")
        
        print("\n🚀 Iniciando dibujo...")
        
        for turn in range(turns):
            agent = agent1 if turn % 2 == 0 else agent2
            
            try:
                move = agent.make_move(turn)
                
                self.clear_screen()
                print(f"Turno {turn + 1}/{turns}")
                print(f"Agente: {agent.name}")
                print(f"Símbolo: '{move['symbol']}'")
                print(f"Posición: ({move['x']}, {move['y']})")
                print()
                
                # Mostrar canvas
                for row in self.canvas.grid:
                    print(''.join(row))
                
                time.sleep(delay)
                
            except KeyboardInterrupt:
                print("\n⏹️ Proceso interrumpido")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                break
        
        print("\n✅ Dibujo completado!")
        
        # Guardar
        save = input("¿Guardar arte? (s/n): ").lower()
        if save == 's':
            filename = input("Nombre del archivo (default: arte_ascii): ") or "arte_ascii"
            with open(f"{filename}.txt", 'w') as f:
                f.write(f"=== ARTE ASCII - {agent1_name} vs {agent2_name} ===\n\n")
                for row in self.canvas.grid:
                    f.write(''.join(row) + '\n')
            print(f"✅ Guardado como {filename}.txt")

if __name__ == "__main__":
    debug = DebugApp()
    
    print("🔧 DEBUG DE AGENTE DIBUJA")
    print("=" * 40)
    
    print("\nOpciones:")
    print("1. Sesión de debug completa")
    print("2. Demo simple")
    print("3. Modo interactivo")
    print("4. Salir")
    
    choice = input("\nSelecciona opción (1-4): ").strip()
    
    if choice == "1":
        debug.run_debug_session()
    elif choice == "2":
        debug.simple_drawing_demo()
    elif choice == "3":
        debug.interactive_mode()
    elif choice == "4":
        print("👋 ¡Hasta luego!")
    else:
        print("❌ Opción no válida")
