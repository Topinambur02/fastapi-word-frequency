.PHONY: run test clean build lint help build-docker run-docker

PYTHON = uv run python
UV     = uv
NAME_IMAGE = fastapi-word-frequency

run:
	$(PYTHON) main.py

run-docker:
	docker run -p 8000:8000 $(NAME_IMAGE)

test:
	$(UV) run pytest -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .coverage
	rm -rf htmlcov/

build:
	$(UV) build

build-docker:
	docker build -t $(NAME_IMAGE):latest .

lint:
	$(UV) run black .

help:
	@echo "Доступные команды:"
	@echo "  make run    		- Запустить приложение (main.py)"
	@echo "  make test   		- Запустить тесты (pytest)"
	@echo "  make clean  		- Удалить кэш и артефакты сборки"
	@echo "  make build  		- Собрать пакет (uv build)"
	@echo "  make lint   		- Проверить код линтером (black)"
	@echo "  make help   		- Показать эту справку"
	@echo "  make run-docker 	- Запустить приложение в докере"
	@echo "  make build-docker 	- Собрать приложение в докере"