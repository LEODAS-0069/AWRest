#!/bin/bash
# Start the Labubu Marketplace application using Docker Compose

set -e

echo "🚀 Starting Labubu Marketplace..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "✅ .env created. Please update it with your configuration."
    echo ""
fi

# Create Docker images
echo "📦 Building Docker images..."
docker-compose build

echo ""
echo "🐳 Starting containers with Docker Compose..."
docker-compose up -d

echo ""
echo "✅ Labubu Marketplace is starting up!"
echo ""
echo "📍 Service URLs:"
echo "   - Frontend:      http://localhost:8000"
echo "   - API Gateway:   http://localhost:5000"
echo "   - Tornado:       http://localhost:8001"
echo "   - Chatbot:       http://localhost:7860"
echo "   - MongoDB:       localhost:27017"
echo "   - PostgreSQL:    localhost:5432"
echo ""
echo "💡 To view logs: docker-compose logs -f"
echo "💡 To stop:      docker-compose down"
