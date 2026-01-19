.PHONY: install install-dev lint format test pre-commit-install clean run-api run-ui type-check coverage help

help:  ## عرض المساعدة
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## تثبيت المشروع
	python -m pip install --upgrade pip
	pip install poetry
	poetry install --no-interaction

install-dev:  ## تثبيت dependencies التطوير
	poetry install

lint:  ## فحص الكود (ruff)
	poetry run ruff check .

format:  ## تنسيق الكود (black + ruff)
	poetry run black .
	poetry run ruff check --fix .

test:  ## تشغيل الاختبارات
	poetry run pytest -v

test-coverage:  ## تشغيل الاختبارات مع coverage
	poetry run pytest --cov=src --cov-report=html --cov-report=term

type-check:  ## فحص الأنواع (mypy)
	poetry run mypy src/

pre-commit-install:  ## تثبيت pre-commit hooks
	poetry run pre-commit install
	poetry run pre-commit run --all-files

clean:  ## تنظيف الملفات المؤقتة
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf htmlcov coverage.xml .coverage

run-api:  ## تشغيل API
	poetry run uvicorn src.sa.api.routes:app --reload --host 0.0.0.0 --port 8000

run-ui:  ## تشغيل Streamlit UI
	poetry run streamlit run src/sa/ui/app.py

docker-build:  ## بناء Docker image
	docker-compose build

docker-up:  ## تشغيل Docker containers
	docker-compose up -d

docker-down:  ## إيقاف Docker containers
	docker-compose down

docker-logs:  ## عرض Docker logs
	docker-compose logs -f

all-checks:  ## تشغيل جميع الفحوصات
	make lint
	make type-check
	make test
