#!/bin/bash

echo "🚀 Starting Collabio Frontend..."

# Navigate to frontend directory
cd "$(dirname "$0")/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo "✅ Dependencies installed"
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env from template..."
    cp .env.example .env 2>/dev/null || echo "VITE_API_BASE_URL=http://localhost:5000/api/v1" > .env
    echo "✅ .env file created"
fi

echo ""
echo "✨ Frontend starting on http://localhost:5173"
echo "🔗 Connected to backend: http://localhost:5000"
echo ""

# Start Vite development server
npm run dev
