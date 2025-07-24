import gradio as gr
import asyncio
import json
import time
from typing import List, Dict, Any, Optional
from openai import OpenAI
import threading
import queue
from dataclasses import dataclass
import numpy as np

# Importar nuestras clases
from canvas import Canvas
from agent import DrawingAgent
from config import Config

@dataclass
class DrawingState:
    canvas: Canvas
    agent1: Optional[DrawingAgent] = None
    agent2: Optional[DrawingAgent] = None
    is_running: bool = False
    current_turn: int = 0
    max_turns: int = 50
    delay: float = 1.0
    messages: List[str] = None
    
    def __post_init__(self):
        if self.messages is None:
            self.messages = []

class GradioInterface:
    def __init__(self):
        self.config = Config()
        self.state = DrawingState(
            canvas=Canvas(self.config.CANVAS_WIDTH, self.config.CANVAS_HEIGHT)
        )
        self.client = None
        self.update_queue = queue.Queue()
        self.setup_complete = False
        
    def setup_lm_studio(self, base_url: str, api_key: str) -> Dict[str, Any]:
        """Configurar conexión con LM Studio"""
        try:
            self.client = OpenAI(
                base_url=base_url,
                api_key=api_key
            )
            
            # Probar conexión
            response = self.client.chat.completions.create(
                model="local-model",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            
            self.setup_complete = True
            return {"status": "success", "message": "✅ LM Studio conectado correctamente"}
            
        except Exception as e:
            self.setup_complete = False
            return {"status": "error", "message": f"❌ Error: {str(e)}"}
    
    def create_agents(self, agent1_name: str, agent2_name: str, symbols_str: str) -> Dict[str, Any]:
        """Crear agentes con nuevos nombres y símbolos"""
        try:
            if not self.setup_complete:
                return {"status": "error", "message": "❌ Primero configura LM Studio"}
            
            symbols = [s.strip() for s in symbols_str.split(',') if s.strip()]
            if len(symbols) < 3:
                return {"status": "error", "message": "❌ Necesitas al menos 3 símbolos"}
            
            self.state.agent1 = DrawingAgent(agent1_name, self.client, self.state.canvas, symbols)
            self.state.agent2 = DrawingAgent(agent2_name, self.client, self.state.canvas, symbols)
            
            return {
                "status": "success", 
                "message": f"✅ Agentes creados: {agent1_name} y {agent2_name}"
            }
            
        except Exception as e:
            return {"status": "error", "message": f"❌ Error creando agentes: {str(e)}"}
    
    def format_canvas_for_display(self) -> str:
        """Formatear el canvas para mostrar en Gradio"""
        canvas_lines = []
        for row in self.state.canvas.grid:
            line = ''.join(row)
            # Reemplazar espacios con puntos para mejor visibilidad
            line = line.replace(' ', '·')
            canvas_lines.append(line)
        return '\n'.join(canvas_lines)
    
    def get_canvas_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del canvas"""
        patterns = self.state.canvas.analyze_patterns()
        return {
            "filled_percentage": f"{patterns['filled_percentage']:.1f}%",
            "total_moves": patterns['total_moves'],
            "symbol_distribution": json.dumps(patterns['symbol_distribution'], indent=2),
            "empty_percentage": f"{patterns['empty_percentage']:.1f}%"
        }
    
    def get_agents_info(self) -> Dict[str, Any]:
        """Obtener información de los agentes"""
        if not self.state.agent1 or not self.state.agent2:
            return {"agent1": "No creado", "agent2": "No creado"}
        
        return {
            "agent1": self.state.agent1.get_stats(),
            "agent2": self.state.agent2.get_stats()
        }
    
    def reset_canvas(self, width: int, height: int) -> Dict[str, Any]:
        """Resetear canvas con nuevas dimensiones"""
        self.state.canvas = Canvas(width, height)
        self.state.current_turn = 0
        self.state.messages = []
        
        if self.state.agent1 and self.state.agent2:
            self.state.agent1.canvas = self.state.canvas
            self.state.agent2.canvas = self.state.canvas
        
        return {
            "canvas_display": self.format_canvas_for_display(),
            "stats": self.get_canvas_stats(),
            "messages": "🎨 Canvas reseteado con éxito"
        }
    
    def start_drawing(self, max_turns: int, delay: float) -> str:
        """Iniciar el proceso de dibujo"""
        if not self.setup_complete:
            return "❌ Primero configura LM Studio"
        
        if not self.state.agent1 or not self.state.agent2:
            return "❌ Primero crea los agentes"
        
        if self.state.is_running:
            return "⚠️ El dibujo ya está en progreso"
        
        self.state.max_turns = max_turns
        self.state.delay = delay
        self.state.is_running = True
        self.state.current_turn = 0
        
        # Iniciar el dibujo en un thread separado
        threading.Thread(target=self._run_drawing_process, daemon=True).start()
        
        return "🎨 Proceso de dibujo iniciado"
    
    def stop_drawing(self) -> str:
        """Detener el proceso de dibujo"""
        self.state.is_running = False
        return "⏹️ Proceso detenido"
    
    def _run_drawing_process(self):
        """Ejecutar el proceso de dibujo"""
        agents = [self.state.agent1, self.state.agent2]
        current_agent_idx = 0
        
        while self.state.is_running and self.state.current_turn < self.state.max_turns:
            try:
                current_agent = agents[current_agent_idx]
                
                # El agente hace su movimiento
                move = asyncio.run(current_agent.make_move(self.state.current_turn))
                
                # Actualizar mensajes
                message = f"Turno {self.state.current_turn + 1}: {current_agent.name} dibujó '{move['symbol']}' en ({move['x']}, {move['y']})"
                self.state.messages.append(message)
                
                # Limitar mensajes
                if len(self.state.messages) > 50:
                    self.state.messages = self.state.messages[-50:]
                
                self.state.current_turn += 1
                current_agent_idx = (current_agent_idx + 1) % 2
                
                # Verificar si el canvas está lleno
                empty_positions = self.state.canvas.get_empty_positions()
                if not empty_positions:
                    self.state.messages.append("🎉 ¡Canvas lleno!")
                    self.state.is_running = False
                    break
                
                time.sleep(self.state.delay)
                
            except Exception as e:
                self.state.messages.append(f"❌ Error: {str(e)}")
                self.state.is_running = False
                break
        
        if self.state.current_turn >= self.state.max_turns:
            self.state.messages.append("⏰ Límite de turnos alcanzado")
        
        self.state.is_running = False
    
    def get_current_state(self) -> Dict[str, Any]:
        """Obtener estado actual para actualizar UI"""
        return {
            "canvas_display": self.format_canvas_for_display(),
            "stats": self.get_canvas_stats(),
            "agents_info": self.get_agents_info(),
            "messages": "\n".join(self.state.messages[-10:]),  # Últimos 10 mensajes
            "current_turn": self.state.current_turn,
            "is_running": self.state.is_running
        }
    
    def save_artwork(self, filename: str) -> str:
        """Guardar el arte actual"""
        if not filename:
            filename = f"arte_ascii_{time.strftime('%Y%m%d_%H%M%S')}"
        
        full_content = f"""🎨 ARTE ASCII COLABORATIVO - INTERFAZ GRADIO
{'='*50}
Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}
Agentes: {self.config.AGENT_1_NAME} y {self.config.AGENT_2_NAME}
Turnos: {self.state.current_turn}

Canvas final:
{self.state.canvas.get_canvas_state()}

Historial de dibujo:
"""
        
        for move in self.state.canvas.draw_history:
            full_content += f"{move['agent']} -> ({move['x']}, {move['y']}) -> '{move['symbol']}'\n"
        
        filepath = f"outputs/{filename}.txt"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        return f"💾 Arte guardado en: {filepath}"

# Crear la aplicación Gradio
def create_gradio_app():
    interface = GradioInterface()
    
    with gr.Blocks(title="🎨 Agente Dibuja - Interfaz Visual", theme=gr.themes.Soft()) as app:
        gr.Markdown("""
        # 🎨 Agente Dibuja - Arte ASCII Multi-Agente
        **Interfaz visual para controlar agentes que dibujan arte ASCII**
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                # Panel de configuración
                with gr.Group():
                    gr.Markdown("### ⚙️ Configuración")
                    
                    with gr.Row():
                        lm_url = gr.Textbox(
                            label="LM Studio URL",
                            value=interface.config.LM_STUDIO_BASE_URL,
                            placeholder="http://localhost:1234/v1"
                        )
                        lm_key = gr.Textbox(
                            label="API Key",
                            value=interface.config.LM_STUDIO_API_KEY,
                            type="password"
                        )
                    
                    setup_btn = gr.Button("🔍 Conectar LM Studio", variant="primary")
                    setup_status = gr.Textbox(label="Estado", interactive=False)
                
                with gr.Group():
                    gr.Markdown("### 🤖 Agentes")
                    
                    agent1_name = gr.Textbox(
                        label="Agente 1",
                        value=interface.config.AGENT_1_NAME
                    )
                    agent2_name = gr.Textbox(
                        label="Agente 2",
                        value=interface.config.AGENT_2_NAME
                    )
                    symbols = gr.Textbox(
                        label="Símbolos (separados por coma)",
                        value=",".join(interface.config.SYMBOLS)
                    )
                    
                    create_agents_btn = gr.Button("🤖 Crear Agentes", variant="secondary")
                    agents_status = gr.Textbox(label="Estado Agentes", interactive=False)
                
                with gr.Group():
                    gr.Markdown("### 🎮 Control")
                    
                    width = gr.Slider(10, 60, interface.config.CANVAS_WIDTH, step=5, label="Ancho Canvas")
                    height = gr.Slider(10, 30, interface.config.CANVAS_HEIGHT, step=5, label="Alto Canvas")
                    max_turns = gr.Slider(10, 100, interface.config.MAX_TURNS, step=10, label="Máximo Turnos")
                    delay = gr.Slider(0.1, 3.0, interface.config.DELAY_ENTRE_TURNOS, step=0.1, label="Delay (segundos)")
                    
                    with gr.Row():
                        start_btn = gr.Button("🚀 Iniciar", variant="primary")
                        stop_btn = gr.Button("⏹️ Detener", variant="stop")
                        reset_btn = gr.Button("🔄 Resetear", variant="secondary")
            
            with gr.Column(scale=3):
                # Canvas visual
                canvas_display = gr.Textbox(
                    label="Canvas ASCII",
                    lines=20,
                    max_lines=30,
                    elem_classes=["monospace"],
                    interactive=False
                )
                
                # Información en tiempo real
                with gr.Row():
                    stats = gr.JSON(label="Estadísticas")
                    agents_info = gr.JSON(label="Agentes")
                
                # Mensajes y logs
                messages = gr.Textbox(
                    label="Logs",
                    lines=10,
                    max_lines=15,
                    interactive=False
                )
                
                # Guardar arte
                with gr.Row():
                    filename = gr.Textbox(label="Nombre archivo", placeholder="arte_personalizado")
                    save_btn = gr.Button("💾 Guardar", variant="secondary")
                    save_status = gr.Textbox(label="Estado Guardado", interactive=False)
        
        # Eventos
        setup_btn.click(
            interface.setup_lm_studio,
            inputs=[lm_url, lm_key],
            outputs=setup_status
        )
        
        create_agents_btn.click(
            interface.create_agents,
            inputs=[agent1_name, agent2_name, symbols],
            outputs=agents_status
        )
        
        reset_btn.click(
            interface.reset_canvas,
            inputs=[width, height],
            outputs=[canvas_display, stats, messages]
        )
        
        start_btn.click(
            interface.start_drawing,
            inputs=[max_turns, delay],
            outputs=messages
        )
        
        stop_btn.click(
            interface.stop_drawing,
            outputs=messages
        )
        
        save_btn.click(
            interface.save_artwork,
            inputs=filename,
            outputs=save_status
        )
        
        # Actualización automática cada segundo
        app.load(
            interface.get_current_state,
            outputs=[canvas_display, stats, agents_info, messages]
        )
        
        # Timer para actualizaciones continuas
        def update_every_second():
            return interface.get_current_state()
        
        # Usar gr.Timer para actualizaciones periódicas
        timer = gr.Timer(1)
        timer.tick(update_every_second, outputs=[canvas_display, stats, agents_info, messages])
    
    return app

if __name__ == "__main__":
    app = create_gradio_app()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True
    )
