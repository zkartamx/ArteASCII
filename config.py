import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configuración LM Studio
    LM_STUDIO_BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
    LM_STUDIO_API_KEY = os.getenv("LM_STUDIO_API_KEY", "not-needed-for-local")
    
    # Configuración del canvas
    CANVAS_WIDTH = int(os.getenv("CANVAS_WIDTH", 40))
    CANVAS_HEIGHT = int(os.getenv("CANVAS_HEIGHT", 20))
    
    # Configuración de agentes
    AGENT_1_NAME = os.getenv("AGENT_1_NAME", "Agente_Azul")
    AGENT_2_NAME = os.getenv("AGENT_2_NAME", "Agente_Rojo")
    MAX_TURNS = int(os.getenv("MAX_TURNS", 50))
    DELAY_ENTRE_TURNOS = float(os.getenv("DELAY_ENTRE_TURNOS", 1.0))
    
    # Símbolos ASCII para dibujar
    SYMBOLS = ['█', '▓', '▒', '░', '▄', '▀', '▌', '▐', '•', '*', '+', '#', '@', '■', '□', '▪', '▫']
