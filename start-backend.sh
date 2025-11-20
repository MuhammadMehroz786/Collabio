#!/bin/bash

echo "🚀 Starting Collabio Backend..."

# Navigate to backend directory
cd "$(dirname "$0")/backend"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if [ ! -f "venv/bin/flask" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
fi

# Check if database exists
echo "Checking database connection..."
if ! psql -U postgres -lqt | cut -d \| -f 1 | grep -qw collabio_db; then
    echo "⚠️  Database 'collabio_db' not found!"
    echo "Creating database..."
    createdb -U postgres collabio_db
    echo "✅ Database created"

    echo "Running migrations..."
    psql -U postgres -d collabio_db -f migrations/001_initial_schema.sql
    echo "✅ Migrations complete"
fi

# Create upload directories if they don't exist
mkdir -p uploads/profiles uploads/resumes uploads/logos uploads/courses uploads/attachments
touch uploads/profiles/.gitkeep uploads/resumes/.gitkeep uploads/logos/.gitkeep uploads/courses/.gitkeep uploads/attachments/.gitkeep

echo ""
echo "✨ Backend starting on http://localhost:5000"
echo "📡 WebSocket available on ws://localhost:5000"
echo ""

# Start Flask application
python run.py
