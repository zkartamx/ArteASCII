import gradio as gr
import time
from openai import OpenAI
from canvas import Canvas
from agent import DrawingAgent
from config import Config
import threading
import json

class SimpleGradioApp:
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
            return "✅ LM Studio conectado exitosamente"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def create_agents(self, name1, name2, symbols_str):
        if not self.client:
            return "❌ Primero configura LM Studio"
        
        symbols = [s.strip() for s in symbols_str.split(',')]
        if len(symbols) < 2:
            return "❌ Necesitas al menos 2 símbolos"
        
        self.agent1 = DrawingAgent(name1, self.client, self.canvas, symbols)
        self.agent2 = DrawingAgent(name2, self.client, self.canvas, symbols)
        
        return f"✅ Agentes creados: {name1} y {name2}"
    
    def format_canvas(self):
        lines = []
        for row in self.canvas.grid:
            line = ''.join(row).replace(' ', '·')
            lines.append(line)
        return '\n'.join(lines)
    
    def get_stats(self):
        patterns = self.canvas.analyze_patterns()
        return {
            "canvas_llenado": f"{patterns['filled_percentage']:.1f}%",
            "turnos_completados": self.current_turn,
            "símbolos_usados": json.dumps(patterns['symbol_distribution'])
        }
    
    def start_drawing(self, max_turns, delay):
        if not self.agent1 or not self.agent2:
            return "❌ Primero crea los agentes"
        
        if self.is_running:
            return "⚠️ Ya está en progreso"
        
        self.is_running = True
        self.current_turn = 0
        self.messages = []
        
        def drawing_process():
            agents = [self.agent1, self.agent2]
            idx = 0
            
            while self.is_running and self.current_turn < max_turns:
                try:
                    agent = agents[idx]
                    move = agent.make_move(self.current_turn)
                    
                    msg = f"Turno {self.current_turn+1}: {agent.name} dibujó '{move['symbol']}'"
                    self.messages.append(msg)
                    
                    self.current_turn += 1
                    idx = (idx + 1) % 2
                    
                    time.sleep(delay)
                    
                except Exception as e:
                    self.messages.append(f"❌ Error: {str(e)}")
                    break
            
            self.is_running = False
            self.messages.append("🎨 Proceso completado")
        
        threading.Thread(target=drawing_process, daemon=True).start()
        return "🚀 Dibujo iniciado"
    
    def stop_drawing(self):
        self.is_running = False
        return "⏹️ Proceso detenido"
    
    def reset_canvas(self, width, height):
        self.canvas = Canvas(width, height)
        self.current_turn = 0
        self.messages = []
        if self.agent1 and self.agent2:
            self.agent1.canvas = self.canvas
            self.agent2.canvas = self.canvas
        return self.format_canvas()
    
    def save_artwork(self, filename):
        if not filename:
            filename = f"arte_ascii_{time.strftime('%Y%m%d_%H%M%S')}"
        
        content = f"""🎨 ARTE ASCII COLABORATIVO
{'='*50}
Canvas:
{self.format_canvas()}

Historial:
"""
        for msg in self.messages[-20:]:
            content += f"{msg}\n"
        
        with open(f"outputs/{filename}.txt", 'w') as f:
            f.write(content)
        
        return f"💾 Guardado como outputs/{filename}.txt"

# Crear la aplicación
def create_interface():
    app = SimpleGradioApp()
    
    with gr.Blocks(title="🎨 Agente Dibuja") as demo:
        gr.Markdown("# 🎨 Agente Dibuja - Arte ASCII Multi-Agente")
        
        with gr.Row():
            with gr.Column(scale=1):
                # Configuración
                gr.Markdown("### ⚙️ Configuración")
                lm_url = gr.Textbox(
                    label="LM Studio URL",
                    value="http://localhost:1234/v1",
                    placeholder="http://localhost:1234/v1"
                )
                lm_key = gr.Textbox(
                    label="API Key",
                    value="not-needed-for-local"
                )
                setup_btn = gr.Button("🔍 Conectar")
                setup_status = gr.Textbox(label="Estado", interactive=False)
                
                # Agentes
                gr.Markdown("### 🤖 Agentes")
                name1 = gr.Textbox(label="Agente 1", value="Agente_Azul")
                name2 = gr.Textbox(label="Agente 2", value="Agente_Rojo")
                symbols = gr.Textbox(label="Símbolos", value="█,▓,▒,░,▄,▀,▌,▐")
                create_btn = gr.Button("🤖 Crear")
                agents_status = gr.Textbox(label="Estado", interactive=False)
                
                # Control
                gr.Markdown("### 🎮 Control")
                width = gr.Slider(10, 60, 40, step=5, label="Ancho")
                height = gr.Slider(10, 30, 20, step=5, label="Alto")
                max_turns = gr.Slider(10, 100, 50, step=10, label="Turnos")
                delay = gr.Slider(0.5, 3.0, 1.0, step=0.1, label="Delay")
                
                reset_btn = gr.Button("🔄 Resetear")
                start_btn = gr.Button("🚀 Iniciar", variant="primary")
                stop_btn = gr.Button("⏹️ Detener", variant="secondary")
                
            with gr.Column(scale=2):
                # Canvas
                canvas_display = gr.Textbox(
                    label="Canvas ASCII",
                    lines=20,
                    interactive=False
                )
                
                # Logs
                logs = gr.Textbox(label="Logs", lines=10, interactive=False)
                
                # Guardar
                filename = gr.Textbox(label="Guardar como", placeholder="mi_arte")
                save_btn = gr.Button("💾 Guardar")
                save_status = gr.Textbox(label="Estado", interactive=False)
        
        # Eventos
        setup_btn.click(app.setup_lm_studio, [lm_url, lm_key], setup_status)
        create_btn.click(app.create_agents, [name1, name2, symbols], agents_status)
        reset_btn.click(app.reset_canvas, [width, height], canvas_display)
        start_btn.click(app.start_drawing, [max_turns, delay], logs)
        stop_btn.click(app.stop_drawing, None, logs)
        save_btn.click(app.save_artwork, filename, save_status)
        
        # Actualización periódica
        def update_display():
            return app.format_canvas(), "\n".join(app.messages[-10:]), app.get_stats()
        
        demo.load(update_display, outputs=[canvas_display, logs])
        
        # Timer para actualizaciones
        timer = gr.Timer(2)
        timer.tick(update_display, outputs=[canvas_display, logs])
    
    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch(server_name="0.0.0.0", server_port=7860, debug=True)
