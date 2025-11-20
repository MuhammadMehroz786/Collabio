#!/bin/bash

echo "🚀 Starting Collabio Platform..."
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "📍 Project directory: $SCRIPT_DIR"
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is not installed"
    exit 1
fi

if ! command_exists psql; then
    echo "❌ PostgreSQL is not installed"
    exit 1
fi

echo "✅ All prerequisites satisfied"
echo ""

# Make scripts executable
chmod +x "$SCRIPT_DIR/start-backend.sh"
chmod +x "$SCRIPT_DIR/start-frontend.sh"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 STARTING COLLABIO PLATFORM"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "⚡ This will start:"
echo "   📦 Backend API  → http://localhost:5000"
echo "   🎨 Frontend App → http://localhost:5173"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Detect OS to open terminals appropriately
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "🍎 Detected macOS - Opening Terminal windows..."

    # Start backend in new terminal
    osascript -e "tell application \"Terminal\" to do script \"cd '$SCRIPT_DIR' && ./start-backend.sh\""

    # Wait a bit for backend to start
    sleep 3

    # Start frontend in new terminal
    osascript -e "tell application \"Terminal\" to do script \"cd '$SCRIPT_DIR' && ./start-frontend.sh\""

    echo ""
    echo "✅ Backend and Frontend started in separate Terminal windows"

elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "🐧 Detected Linux - Opening terminal windows..."

    if command_exists gnome-terminal; then
        gnome-terminal -- bash -c "cd '$SCRIPT_DIR' && ./start-backend.sh; exec bash"
        sleep 3
        gnome-terminal -- bash -c "cd '$SCRIPT_DIR' && ./start-frontend.sh; exec bash"
    elif command_exists xterm; then
        xterm -e "cd '$SCRIPT_DIR' && ./start-backend.sh" &
        sleep 3
        xterm -e "cd '$SCRIPT_DIR' && ./start-frontend.sh" &
    else
        echo "⚠️  Could not detect terminal emulator"
        echo "Please run the following commands in separate terminals:"
        echo ""
        echo "Terminal 1: ./start-backend.sh"
        echo "Terminal 2: ./start-frontend.sh"
        exit 0
    fi

    echo ""
    echo "✅ Backend and Frontend started in separate terminal windows"

else
    # Other OS or can't detect
    echo "⚠️  Automatic terminal opening not supported on this OS"
    echo ""
    echo "Please open two separate terminal windows and run:"
    echo ""
    echo "📍 Terminal 1 (Backend):"
    echo "   cd $SCRIPT_DIR"
    echo "   ./start-backend.sh"
    echo ""
    echo "📍 Terminal 2 (Frontend):"
    echo "   cd $SCRIPT_DIR"
    echo "   ./start-frontend.sh"
    exit 0
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 COLLABIO IS STARTING!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📱 Open in browser: http://localhost:5173"
echo ""
echo "💡 Tips:"
echo "   • Backend logs in first terminal window"
echo "   • Frontend logs in second terminal window"
echo "   • Press Ctrl+C in each window to stop servers"
echo ""
echo "📚 Documentation:"
echo "   • Setup Guide: $SCRIPT_DIR/SETUP_GUIDE.md"
echo "   • API Docs: $SCRIPT_DIR/backend/README.md"
echo "   • Frontend Services: $SCRIPT_DIR/frontend/src/services/README.md"
echo ""
