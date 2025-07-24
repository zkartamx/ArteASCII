import gradio as gr
import time
import threading
from openai import OpenAI
from canvas import Canvas
from agent import DrawingAgent
from config import Config

class MinimalGradioApp:
    def __init__(self):
        self.config = Config()
        self.canvas = Canvas(40, 20)
        self.client = None
        self.agent1 = None
        self.agent2 = None
        self.is_running = False
        self.current_turn = 0
        self.messages = []
        
    def setup_lm_studio(self, url, key):
        try:
            self.client = OpenAI(base_url=url, api_key=key)
            self.client.chat.completions.create(
                model="local-model",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1
            )
            return "✅ LM Studio conectado"
        except Exception as e:
            return f"❌ Error: {e}"
    
    def create_agents(self, name1, name2, symbols):
        if not self.client:
            return "❌ Configura LM Studio primero"
        
        symbols_list = [s.strip() for s in symbols.split(',')]
        self.agent1 = DrawingAgent(name1, self.client, self.canvas, symbols_list)
        self.agent2 = DrawingAgent(name2, self.client, self.canvas, symbols_list)
        return f"✅ Agentes: {name1} y {name2}"
    
    def format_canvas(self):
        return '\n'.join([''.join(row) for row in self.canvas.grid])
    
    def start_drawing(self, max_turns, delay):
        if not self.agent1 or not self.agent2:
            return "❌ Crea agentes primero"
        
        self.is_running = True
        self.current_turn = 0
        
        def drawing_loop():
            agents = [self.agent1, self.agent2]
            idx = 0
            
            while self.is_running and self.current_turn < max_turns:
                try:
                    agent = agents[idx]
                    move = agent.make_move(self.current_turn)
                    
                    self.messages.append(f"Turno {self.current_turn+1}: {agent.name} dibujó '{move['symbol']}'")
                    self.current_turn += 1
                    idx = (idx + 1) % 2
                    
                    time.sleep(delay)
                    
                except Exception as e:
                    self.messages.append(f"Error: {e}")
                    break
            
            self.is_running = False
            self.messages.append("🎨 Completado")
        
        threading.Thread(target=drawing_loop, daemon=True).start()
        return "🚀 Iniciado"
    
    def stop_drawing(self):
        self.is_running = False
        return "⏹️ Detenido"
    
    def reset_canvas(self, width, height):
        self.canvas = Canvas(width, height)
        self.current_turn = 0
        self.messages = []
        return self.format_canvas()
    
    def get_current_state(self):
        return self.format_canvas(), "\n".join(self.messages[-5:])

# Crear interfaz muy simple
def create_app():
    app = MinimalGradioApp()
    
    def update_canvas():
        return app.format_canvas(), "\n".join(app.messages[-5:])
    
    with gr.Blocks(title="Agente Dibuja") as demo:
        gr.Markdown("# 🎨 Agente Dibuja")
        
        with gr.Row():
            # Panel izquierdo
            with gr.Column(scale=1):
                gr.Markdown("### Configuración")
                
                url = gr.Textbox("http://localhost:1234/v1", label="LM Studio URL")
                key = gr.Textbox("not-needed-for-local", label="API Key")
                setup_btn = gr.Button("Conectar")
                setup_status = gr.Textbox(label="Estado", interactive=False)
                
                name1 = gr.Textbox("Agente_Azul", label="Agente 1")
                name2 = gr.Textbox("Agente_Rojo", label="Agente 2")
                symbols = gr.Textbox("█,▓,▒,░,▄,▀", label="Símbolos")
                create_btn = gr.Button("Crear Agentes")
                agents_status = gr.Textbox(label="Estado", interactive=False)
                
                width = gr.Slider(10, 50, 40, step=5, label="Ancho")
                height = gr.Slider(10, 30, 20, step=5, label="Alto")
                max_turns = gr.Slider(10, 100, 30, step=10, label="Turnos")
                delay = gr.Slider(0.5, 3.0, 1.0, step=0.1, label="Delay")
                
                reset_btn = gr.Button("Resetear Canvas")
                start_btn = gr.Button("Iniciar", variant="primary")
                stop_btn = gr.Button("Detener")
                
            # Panel derecho
            with gr.Column(scale=2):
                canvas = gr.Textbox(
                    label="Canvas ASCII",
                    lines=20,
                    max_lines=25,
                    interactive=False
                )
                
                logs = gr.Textbox(
                    label="Logs",
                    lines=10,
                    max_lines=15,
                    interactive=False
                )
                
                filename = gr.Textbox("mi_arte", label="Guardar como")
                save_btn = gr.Button("Guardar")
                save_status = gr.Textbox(label="Estado", interactive=False)
        
        # Conectar eventos
        setup_btn.click(app.setup_lm_studio, [url, key], setup_status)
        create_btn.click(app.create_agents, [name1, name2, symbols], agents_status)
        reset_btn.click(app.reset_canvas, [width, height], canvas)
        start_btn.click(app.start_drawing, [max_turns, delay], logs)
        stop_btn.click(app.stop_drawing, None, logs)
        save_btn.click(lambda f: app.save_artwork(f), filename, save_status)
        
        # Actualización periódica
        demo.load(lambda: app.get_current_state(), outputs=[canvas, logs])
        
        # Timer para actualizaciones
        timer = gr.Timer(2)
        timer.tick(lambda: app.get_current_state(), outputs=[canvas, logs])
    
    return demo

if __name__ == "__main__":
    demo = create_app()
    demo.launch(server_name="0.0.0.0", server_port=7860, debug=True)
