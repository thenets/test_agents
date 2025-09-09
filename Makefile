VENV_DIR = ./venv

.PHONY: help venv install clean test run-basic run-langgraph notebook

# Default target
help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

venv: ## Create virtual environment and install dependencies
	@echo "Creating virtual environment..."
	python -m venv $(VENV_DIR)
	@echo "Activating virtual environment and installing dependencies..."
	$(VENV_DIR)/bin/pip install --upgrade pip
	$(VENV_DIR)/bin/pip install -r requirements.txt
	@echo "Setup complete! To activate the environment, run:"
	@echo "source $(VENV_DIR)/bin/activate"

install: ## Install dependencies in existing environment
	@echo "Installing dependencies..."
	pip install --upgrade pip
	pip install -r requirements.txt
	@echo "Dependencies installed!"

clean: ## Remove virtual environment and cache files
	@echo "Removing virtual environment..."
	rm -rf $(VENV_DIR)
	@echo "Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete
	@echo "Cleanup complete!"

test: ## Run basic tests on examples
	@echo "Testing basic examples..."
	cd examples/basic/01_simple_react_agent && python -c "import main; print(' 01_simple_react_agent imports OK')"
	cd examples/basic/02_search_agent && python -c "import main; print(' 02_search_agent imports OK')"
	cd examples/langgraph/02_tool_integration_calculator && python -c "import main; print(' 02_tool_integration_calculator imports OK')"
	@echo "All import tests passed!"

run-basic: ## Run all basic examples
	@echo "Running basic examples..."
	cd examples/basic/01_simple_react_agent && python main.py
	cd examples/basic/02_search_agent && python main.py
	cd examples/basic/03_controller_agent && python main.py
	cd examples/basic/04_persona_agent && python main.py

run-langgraph: ## Run all LangGraph examples
	@echo "Running LangGraph examples..."
	cd examples/langgraph/01_structured_output_openrouter && python main.py
	cd examples/langgraph/02_tool_integration_calculator && python main.py
	cd examples/langgraph/03_simple_agent_loop && python main.py

notebook: ## Start Jupyter notebook server
	@echo "Starting Jupyter notebook server..."
	jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root