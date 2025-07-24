import gradio as gr
import time
import threading
from openai import OpenAI
from canvas import Canvas
from agent import DrawingAgent

# Configuración simple
class ArtCanvas:
    def __init__(self):
        self.canvas = Canvas(30, 15)
        self.client = None
        self.agent1 = None
        self.agent2 = None
        self.messages = []
        
    def connect(self, url):
        try:
            self.client = OpenAI(base_url=url, api_key="not-needed")
            return "✅ Conectado"
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
        
        def draw():
            agents = [self.agent1, self.agent2]
            idx = 0
            
            for turn in range(turns):
                agent = agents[idx]
                try:
                    move = agent.make_move(turn)
                    self.messages.append(f"Turno {turn+1}: {agent.name} dibujó '{move['symbol']}'")
                    time.sleep(delay)
                    idx = (idx + 1) % 2
                except Exception as e:
                    self.messages.append(f"Error: {e}")
                    break
            
            self.messages.append("🎨 Completado")
        
        threading.Thread(target=draw, daemon=True).start()
        return "🚀 Iniciado"
    
    def reset_canvas(self):
        self.canvas = Canvas(30, 15)
        self.messages = []
        return self.format_canvas()
    
    def format_canvas(self):
        return '\n'.join([''.join(row) for row in self.canvas.grid])
    
    def get_logs(self):
        return '\n'.join(self.messages[-8:])

# Instancia global
art_app = ArtCanvas()

# Crear interfaz ultra-simple
def create_simple_interface():
    with gr.Blocks(title="Agente Dibuja - Arte ASCII") as demo:
        gr.Markdown("# 🎨 Agente Dibuja - Arte ASCII")
        
        # Canvas principal
        canvas_display = gr.Textbox(
            label="Canvas ASCII",
            lines=15,
            interactive=False
        )
        
        logs_display = gr.Textbox(
            label="Logs",
            lines=8,
            interactive=False
        )
        
        with gr.Row():
            with gr.Column():
                lm_url = gr.Textbox(
                    "http://localhost:1234/v1",
                    label="LM Studio URL"
                )
                connect_btn = gr.Button("🔍 Conectar")
                
                agent1 = gr.Textbox("Agente_Azul", label="Agente 1")
                agent2 = gr.Textbox("Agente_Rojo", label="Agente 2")
                create_btn = gr.Button("🤖 Crear Agentes")
                
                turns = gr.Slider(5, 50, 20, step=5, label="Turnos")
                delay = gr.Slider(0.5, 3.0, 1.0, step=0.1, label="Delay")
                
                start_btn = gr.Button("🚀 Iniciar", variant="primary")
                reset_btn = gr.Button("🔄 Resetear")
                
            with gr.Column():
                status = gr.Textbox(label="Estado", interactive=False)
        
        # Funciones de actualización
        def update_display():
            return art_app.format_canvas(), art_app.get_logs()
        
        # Conectar eventos
        connect_btn.click(art_app.connect, lm_url, status)
        create_btn.click(art_app.create_agents, [agent1, agent2], status)
        start_btn.click(art_app.start_drawing, [turns, delay], status)
        reset_btn.click(art_app.reset_canvas, None, canvas_display)
        
        # Actualización automática
        demo.load(update_display, outputs=[canvas_display, logs_display])
        
        # Timer para actualizaciones suaves
        timer = gr.Timer(2)
        timer.tick(update_display, outputs=[canvas_display, logs_display])
    
    return demo

if __name__ == "__main__":
    demo = create_simple_interface()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        debug=False,
        show_error=False
    )
