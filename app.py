import gradio as gr
import time
import threading
from openai import OpenAI
from canvas import Canvas
from agent import DrawingAgent
import json

# Configuración global
CANVAS_WIDTH = 30
CANVAS_HEIGHT = 15

class SimpleAgentApp:
    def __init__(self):
        self.canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
        self.client = None
        self.agent1 = None
        self.agent2 = None
        self.is_running = False
        self.messages = []
        
    def connect_lm_studio(self, url):
        try:
            self.client = OpenAI(base_url=url, api_key="not-needed")
            return "✅ Conectado a LM Studio"
        except Exception as e:
            return f"❌ Error: {e}"
    
    def create_agents(self, name1, name2):
        if not self.client:
            return "❌ Primero conecta LM Studio"
        
        symbols = ["█", "▓", "▒", "░", "▄", "▀", "▌", "▐", "•", "+"]
        self.agent1 = DrawingAgent(name1, self.client, self.canvas, symbols)
        self.agent2 = DrawingAgent(name2, self.client, self.canvas, symbols)
        return f"✅ Agentes creados: {name1} y {name2}"
    
    def start_drawing(self, turns, delay):
        if not self.agent1 or not self.agent2:
            return "❌ Crea agentes primero"
        
        self.is_running = True
        
        def draw():
            agents = [self.agent1, self.agent2]
            idx = 0
            
            for turn in range(turns):
                if not self.is_running:
                    break
                
                agent = agents[idx]
                try:
                    move = agent.make_move(turn)
                    self.messages.append(f"Turno {turn+1}: {agent.name} dibujó '{move['symbol']}'")
                    idx = (idx + 1) % 2
                    time.sleep(delay)
                except Exception as e:
                    self.messages.append(f"Error: {e}")
                    break
            
            self.is_running = False
            self.messages.append("🎨 Completado")
        
        threading.Thread(target=draw, daemon=True).start()
        return "🚀 Dibujo iniciado"
    
    def stop_drawing(self):
        self.is_running = False
        return "⏹️ Detenido"
    
    def reset_canvas(self):
        self.canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
        self.messages = []
        return self.format_canvas()
    
    def format_canvas(self):
        return '\n'.join([''.join(row) for row in self.canvas.grid])
    
    def get_stats(self):
        patterns = self.canvas.analyze_patterns()
        return f"Canvas llenado: {patterns['filled_percentage']:.1f}%"

# Instancia global
app = SimpleAgentApp()

def create_interface():
    with gr.Blocks(title="Agente Dibuja - Arte ASCII") as demo:
        gr.Markdown("# 🎨 Agente Dibuja - Arte ASCII Multi-Agente")
        
        # Estado actual
        canvas_display = gr.Textbox(
            label="Canvas ASCII",
            lines=15,
            max_lines=15,
            interactive=False
        )
        
        logs_display = gr.Textbox(
            label="Logs",
            lines=8,
            max_lines=8,
            interactive=False
        )
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Configuración")
                lm_url = gr.Textbox("http://localhost:1234/v1", label="LM Studio URL")
                connect_btn = gr.Button("Conectar a LM Studio")
                connect_status = gr.Textbox(label="Estado", interactive=False)
                
                agent1_name = gr.Textbox("Agente_Azul", label="Agente 1")
                agent2_name = gr.Textbox("Agente_Rojo", label="Agente 2")
                create_btn = gr.Button("Crear Agentes")
                agents_status = gr.Textbox(label="Estado", interactive=False)
                
                turns = gr.Slider(5, 50, 20, step=5, label="Máximo de turnos")
                delay = gr.Slider(0.5, 2.0, 1.0, step=0.1, label="Delay (segundos)")
                
                with gr.Row():
                    start_btn = gr.Button("🚀 Iniciar", variant="primary")
                    stop_btn = gr.Button("⏹️ Detener", variant="secondary")
                    reset_btn = gr.Button("🔄 Resetear")
        
        # Funciones para actualizar
        def update_display():
            return app.format_canvas(), "\n".join(app.messages[-5:])
        
        # Conectar eventos
        connect_btn.click(app.connect_lm_studio, lm_url, connect_status)
        create_btn.click(app.create_agents, [agent1_name, agent2_name], agents_status)
        start_btn.click(app.start_drawing, [turns, delay], logs_display)
        stop_btn.click(app.stop_drawing, None, logs_display)
        reset_btn.click(app.reset_canvas, None, canvas_display)
        
        # Actualización automática
        demo.load(update_display, outputs=[canvas_display, logs_display])
        
        # Timer para actualizaciones periódicas
        timer = gr.Timer(2)
        timer.tick(update_display, outputs=[canvas_display, logs_display])
    
    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        debug=False,
        share=False
    )
