#!/usr/bin/env python3
import asyncio
import time
from openai import OpenAI
from canvas import Canvas
from agent import DrawingAgent
from config import Config
import os

class ArtCollaboration:
    def __init__(self):
        self.config = Config()
        self.setup_lm_studio()
        
        # Inicializar canvas
        self.canvas = Canvas(self.config.CANVAS_WIDTH, self.config.CANVAS_HEIGHT)
        
        # Inicializar clientes OpenAI para cada agente
        self.client = OpenAI(
            base_url=self.config.LM_STUDIO_BASE_URL,
            api_key=self.config.LM_STUDIO_API_KEY
        )
        
        # Crear agentes
        self.agent1 = DrawingAgent(
            self.config.AGENT_1_NAME,
            self.client,
            self.canvas,
            self.config.SYMBOLS
        )
        
        self.agent2 = DrawingAgent(
            self.config.AGENT_2_NAME,
            self.client,
            self.canvas,
            self.config.SYMBOLS
        )
        
        self.current_turn = 0
        self.agents = [self.agent1, self.agent2]
        self.current_agent_index = 0
    
    def setup_lm_studio(self):
        """Verificar conexión con LM Studio"""
        try:
            print("🔍 Verificando conexión con LM Studio...")
            test_client = OpenAI(
                base_url=self.config.LM_STUDIO_BASE_URL,
                api_key=self.config.LM_STUDIO_API_KEY
            )
            test_client.chat.completions.create(
                model="local-model",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            print("✅ LM Studio está conectado y funcionando")
        except Exception as e:
            print(f"❌ Error conectando a LM Studio: {e}")
            print("📝 Asegúrate de que LM Studio esté ejecutándose en http://localhost:1234")
            exit(1)
    
    async def run_collaboration(self):
        """Ejecutar la colaboración entre agentes"""
        print(f"🎨 Iniciando colaboración artística")
        print(f"Agente 1: {self.config.AGENT_1_NAME}")
        print(f"Agente 2: {self.config.AGENT_2_NAME}")
        print(f"Canvas: {self.config.CANVAS_WIDTH}x{self.config.CANVAS_HEIGHT}")
        print(f"Máximo de turnos: {self.config.MAX_TURNS}")
        print("-" * 50)
        
        while self.current_turn < self.config.MAX_TURNS:
            current_agent = self.agents[self.current_agent_index]
            
            # Mostrar canvas actual
            self.canvas.display(current_agent.name)
            
            # Agente actual hace su movimiento
            print(f"\n🤖 Turno {self.current_turn + 1} - {current_agent.name}")
            
            try:
                move = await current_agent.make_move(self.current_turn)
                print(f"   ✏️ Dibujó '{move['symbol']}' en ({move['x']}, {move['y']})")
                print(f"   💭 Razón: {move['reason']}")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                continue
            
            # Esperar antes del siguiente turno
            await asyncio.sleep(self.config.DELAY_ENTRE_TURNOS)
            
            # Siguiente turno
            self.current_turn += 1
            self.current_agent_index = (self.current_agent_index + 1) % 2
            
            # Verificar si el canvas está lleno
            empty_positions = self.canvas.get_empty_positions()
            if not empty_positions:
                print("\n🎉 ¡Canvas lleno! La obra está completa.")
                break
        
        # Mostrar resultado final
        self.canvas.display()
        self.show_final_stats()
    
    def show_final_stats(self):
        """Mostrar estadísticas finales"""
        stats = self.canvas.analyze_patterns()
        
        print("\n" + "="*50)
        print("📊 ESTADÍSTICAS FINALES")
        print("="*50)
        print(f"Turnos jugados: {self.current_turn}")
        print(f"Canvas llenado: {stats['filled_percentage']:.1f}%")
        print(f"Distribución de símbolos: {stats['symbol_distribution']}")
        
        print(f"\n📈 Estadísticas por agente:")
        for agent in self.agents:
            agent_stats = agent.get_stats()
            print(f"  {agent_stats['name']}:")
            print(f"    - Movimientos: {agent_stats['total_moves']}")
            print(f"    - Estilo: {agent_stats['style']['approach']}")
            print(f"    - Preferencia: {agent_stats['style']['preference']}")
        
        # Guardar resultado final
        self.save_final_art()
    
    def save_final_art(self):
        """Guardar el arte final en un archivo"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"arte_ascii_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("🎨 ARTE ASCII COLABORATIVO\n")
            f.write("=" * 50 + "\n")
            f.write(f"Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Agentes: {self.config.AGENT_1_NAME} y {self.config.AGENT_2_NAME}\n")
            f.write(f"Turnos: {self.current_turn}\n\n")
            
            f.write("Canvas final:\n")
            f.write(self.canvas.get_canvas_state())
            
            f.write("\n\nHistorial de dibujo:\n")
            for move in self.canvas.draw_history:
                f.write(f"{move['agent']} -> ({move['x']}, {move['y']}) -> '{move['symbol']}'\n")
        
        print(f"\n💾 Arte guardado en: {filename}")

async def main():
    """Función principal"""
    collaboration = ArtCollaboration()
    await collaboration.run_collaboration()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n
⏹️ Colaboración interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
