.PHONY: help install run test clean migrate seed docker-up docker-down

# Default target
help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make run          - Run the development server"
	@echo "  make clean        - Clean up generated files"
	@echo "  make migrate      - Run database migrations"
	@echo "  make seed         - Seed database with sample data"
	@echo "  make docker-up    - Start Docker containers"
	@echo "  make docker-down  - Stop Docker containers"
	@echo "  make format       - Format code with black and isort"
	@echo "  make lint         - Run code linting"

# Install dependencies
install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

# Run development server
run:
	python main.py

# Clean up generated files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

# Database migrations
migrate:
	flask db migrate
	flask db upgrade

# Initialize migrations
init-migrate:
	flask db init
	flask db migrate -m "Initial migration"
	flask db upgrade

# Seed database
seed:
	flask seed-db

# Initialize database
init-db:
	flask init-db

# Drop database
drop-db:
	flask drop-db

# Docker commands
docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-build:
	docker-compose build

# Code formatting
format:
	black app/ tests/
	isort app/ tests/

# Code linting
lint:
	flake8 app/ tests/
	black --check app/ tests/
	isort --check-only app/ tests/

# Create virtual environment
venv:
	python -m venv venv
	@echo "Virtual environment created. Activate it with:"
	@echo "  source venv/bin/activate  (Linux/Mac)"
	@echo "  venv\\Scripts\\activate     (Windows)"

# Setup development environment
setup: venv install init-migrate seed
	@echo "Development environment setup complete!"