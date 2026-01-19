#!/bin/bash
set -e

echo "🚀 Setting up SA development environment..."

# Install dependencies with Poetry
echo "📦 Installing Python dependencies..."
poetry install --no-interaction

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env file with your API keys!"
else
    echo "ℹ️  .env file already exists, skipping creation"
fi

# Create output directories
echo "📁 Creating output directories..."
mkdir -p outputs/images outputs/videos outputs/audio logs data

# Install pre-commit hooks
echo "🔧 Installing pre-commit hooks..."
poetry run pre-commit install || true

# Run initial checks
echo "✅ Running initial code quality checks..."
poetry run black --check . || echo "ℹ️  Run 'make format' to auto-format code"
poetry run ruff check . || echo "ℹ️  Run 'make lint' to see linting issues"

# Display helpful information
echo ""
echo "✨ SA Development Environment is ready!"
echo ""
echo "🧪 Test the environment:"
echo "  python .devcontainer/test_environment.py"
echo ""
echo "📚 Quick commands:"
echo "  make run-ui          # Start Streamlit UI (port 8501)"
echo "  make run-api         # Start FastAPI backend (port 8000)"
echo "  make test            # Run tests"
echo "  make format          # Format code"
echo "  make lint            # Check code quality"
echo "  make help            # Show all available commands"
echo ""
echo "🔑 Don't forget to add your API keys to .env file!"
echo ""
