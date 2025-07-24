import gradio as gr
import time
import threading
from openai import OpenAI
from canvas import Canvas
from agent import DrawingAgent

# Versión web ultra-simple con estilos básicos
class WebApp:
    def __init__(self):
        self.canvas = Canvas(25, 12)
        self.client = None
        self.agent1 = None
        self.agent2 = None
        self.running = False
        self.logs = []
        
    def connect_lm_studio(self, url):
        try:
            self.client = OpenAI(base_url=url, api_key="not-needed")
            return "✅ LM Studio conectado"
        except Exception as e:
            return f"❌ Error: {e}"
    
    def create_agents(self, name1, name2):
        if not self.client:
            return "❌ Primero conecta LM Studio"
        
        symbols = ["█", "▓", "▒", "░", "▄", "▀"]
        self.agent1 = DrawingAgent(name1, self.client, self.canvas, symbols)
        self.agent2 = DrawingAgent(name2, self.client, self.canvas, symbols)
        return f"✅ Agentes: {name1} y {name2}"
    
    def start_drawing(self, turns, delay):
        if not self.agent1 or not self.agent2:
            return "❌ Crea agentes primero"
        
        self.running = True
        
        def draw():
            agents = [self.agent1, self.agent2]
            idx = 0
            
            for turn in range(turns):
                if not self.running:
                    break
                
                agent = agents[idx]
                try:
                    move = agent.make_move(turn)
                    self.logs.append(f"Turno {turn+1}: {agent.name} dibujó '{move['symbol']}'")
                    idx = (idx + 1) % 2
                    time.sleep(delay)
                except Exception as e:
                    self.logs.append(f"Error: {e}")
                    break
            
            self.logs.append("🎨 Completado")
            self.running = False
        
        threading.Thread(target=draw, daemon=True).start()
        return "🚀 Iniciado"
    
    def stop_drawing(self):
        self.running = False
        return "⏹️ Detenido"
    
    def reset_canvas(self):
        self.canvas = Canvas(25, 12)
        self.logs = []
        return self.format_canvas()
    
    def format_canvas(self):
        return '\n'.join([''.join(row) for row in self.canvas.grid])
    
    def get_logs(self):
        return '\n'.join(self.logs[-6:])

app = WebApp()

def create_web_interface():
    with gr.Blocks(
        title="Agente Dibuja",
        theme=gr.themes.Soft()
    ) as interface:
        
        gr.Markdown("# 🎨 Agente Dibuja - Arte ASCII")
        
        with gr.Row(equal_height=True):
            # Panel de control
            with gr.Column(scale=1):
                gr.Markdown("### 🔧 Configuración")
                
                lm_url = gr.Textbox(
                    value="http://localhost:1234/v1",
                    label="LM Studio URL",
                    placeholder="http://localhost:1234/v1"
                )
                connect_btn = gr.Button("🔗 Conectar", variant="secondary")
                connect_status = gr.Textbox(label="Estado", interactive=False)
                
                gr.Markdown("### 🤖 Agentes")
                agent1_name = gr.Textbox("Agente_Azul", label="Agente 1")
                agent2_name = gr.Textbox("Agente_Rojo", label="Agente 2")
                create_agents_btn = gr.Button("👥 Crear Agentes")
                agents_status = gr.Textbox(label="Estado", interactive=False)
                
                gr.Markdown("### ⚙️ Opciones")
                turns_slider = gr.Slider(5, 30, 15, step=5, label="Turnos")
                delay_slider = gr.Slider(0.5, 2.0, 1.0, step=0.1, label="Delay (segundos)")
                
                with gr.Row():
                    start_btn = gr.Button("🚀 Iniciar", variant="primary")
                    stop_btn = gr.Button("⏹️ Detener", variant="stop")
                    reset_btn = gr.Button("🔄 Resetear", variant="secondary")
            
            # Panel de visualización
            with gr.Column(scale=2):
                gr.Markdown("### 🎨 Canvas ASCII")
                canvas_display = gr.Textbox(
                    label="",
                    lines=12,
                    max_lines=12,
                    interactive=False,
                    show_label=False
                )
                
                gr.Markdown("### 📋 Logs")
                logs_display = gr.Textbox(
                    label="",
                    lines=8,
                    max_lines=8,
                    interactive=False,
                    show_label=False
                )
    
    # Funciones de actualización
    def update_display():
        return app.format_canvas(), app.get_logs()
    
    # Conectar eventos
    connect_btn.click(app.connect_lm_studio, lm_url, connect_status)
    create_agents_btn.click(app.create_agents, [agent1_name, agent2_name], agents_status)
    start_btn.click(app.start_drawing, [turns_slider, delay_slider], logs_display)
    stop_btn.click(app.stop_drawing, None, logs_display)
    reset_btn.click(app.reset_canvas, None, canvas_display)
    
    # Actualización automática
    interface.load(update_display, outputs=[canvas_display, logs_display])
    
    # Timer para actualizaciones suaves
    timer = gr.Timer(1.5)
    timer.tick(update_display, outputs=[canvas_display, logs_display])
    
    return interface

if __name__ == "__main__":
    demo = create_web_interface()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        debug=False,
        show_error=False,
        show_api=False
    )
