# Makefile para Agente Dibuja
.PHONY: help install run-local run-docker build-docker clean setup venv

# Variables
PYTHON := python3
VENV := .venv
VENV_BIN := $(VENV)/bin
DOCKER_IMAGE := agente-dibuja:latest

# Colores para output
GREEN := \033[0;32m
BLUE := \033[0;34m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Mostrar esta ayuda
	@echo "$(BLUE)Agente Dibuja - Comandos disponibles:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

setup: ## Configuración inicial completa
	@echo "$(BLUE)🚀 Configurando Agente Dibuja...$(NC)"
	@$(PYTHON) setup.py

venv: ## Crear entorno virtual
	@echo "$(BLUE)📦 Creando entorno virtual...$(NC)"
	@$(PYTHON) -m venv $(VENV)
	@echo "$(GREEN)✅ Entorno virtual creado$(NC)"

install: venv ## Instalar dependencias en entorno virtual
	@echo "$(BLUE)📦 Instalando dependencias...$(NC)"
	@$(VENV_BIN)/pip install --upgrade pip
	@$(VENV_BIN)/pip install -r requirements.txt
	@echo "$(GREEN)✅ Dependencias instaladas$(NC)"

install-local: ## Instalar dependencias localmente (sin venv)
	@echo "$(BLUE)📦 Instalando dependencias localmente...$(NC)"
	@$(PYTHON) -m pip install -r requirements.txt

run-local: ## Ejecutar con entorno virtual
	@echo "$(BLUE)🎨 Ejecutando Agente Dibuja (local)...$(NC)"
	@$(VENV_BIN)/python main.py

run-docker: ## Ejecutar con Docker
	@echo "$(BLUE)🐳 Ejecutando con Docker...$(NC)"
	@docker-compose up --build

build-docker: ## Construir imagen Docker
	@echo "$(BLUE)🔨 Construyendo imagen Docker...$(NC)"
	@docker build -t $(DOCKER_IMAGE) .

run-docker-bg: ## Ejecutar Docker en segundo plano
	@echo "$(BLUE)🐳 Ejecutando Docker en segundo plano...$(NC)"
	@docker-compose up --build -d

stop-docker: ## Detener Docker
	@echo "$(RED)⏹️  Deteniendo Docker...$(NC)"
	@docker-compose down

clean: ## Limpiar archivos generados y entornos
	@echo "$(RED)🧹 Limpiando...$(NC)"
	@rm -rf $(VENV)
	@rm -rf __pycache__
	@rm -rf *.pyc
	@rm -rf outputs/*.txt
	@docker-compose down -v
	@docker rmi $(DOCKER_IMAGE) 2>/dev/null || true
	@echo "$(GREEN)✅ Limpieza completada$(NC)"

logs: ## Ver logs de Docker
	@docker-compose logs -f

shell: ## Entrar al contenedor Docker
	@docker-compose exec agente-dibuja /bin/sh

check-lm-studio: ## Verificar conexión con LM Studio
	@echo "$(BLUE)🔍 Verificando conexión con LM Studio...$(NC)"
	@curl -s http://localhost:1234/v1/models | jq . 2>/dev/null || echo "$(RED)❌ LM Studio no está respondiendo$(NC)"

# Comandos rápidos
run: run-local ## Alias para run-local
docker: run-docker ## Alias para run-docker

# Comandos de desarrollo
dev: install ## Instalar y preparar para desarrollo
	@echo "$(GREEN)✅ Listo para desarrollo$(NC)"

test: ## Ejecutar pruebas básicas
	@echo "$(BLUE)🧪 Ejecutando pruebas...$(NC)"
	@$(PYTHON) -c "import config; print('✅ Configuración válida')"
	@$(PYTHON) -c "from canvas import Canvas; c = Canvas(5,5); print('✅ Canvas funciona')"
	@echo "$(GREEN)✅ Pruebas pasadas$(NC)"
