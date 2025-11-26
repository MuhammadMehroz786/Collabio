#!/bin/bash

# Collabio Demo Mode Launcher
# Starts the frontend in demo mode with mock data

echo "======================================"
echo "  Collabio - Demo Mode"
echo "======================================"
echo ""
echo "Starting frontend with mock data..."
echo "No backend required!"
echo ""

# Navigate to frontend directory
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Ensure demo mode is enabled
if ! grep -q "VITE_DEMO_MODE=true" .env; then
    echo "Enabling demo mode..."
    if grep -q "VITE_DEMO_MODE" .env; then
        # Replace existing VITE_DEMO_MODE line
        sed -i '' 's/VITE_DEMO_MODE=.*/VITE_DEMO_MODE=true/' .env
    else
        # Add VITE_DEMO_MODE line
        echo "" >> .env
        echo "# Demo Mode - Set to 'true' to use mock data without backend" >> .env
        echo "VITE_DEMO_MODE=true" >> .env
    fi
fi

echo ""
echo "✅ Demo mode enabled"
echo ""
echo "======================================"
echo "  Demo Credentials"
echo "======================================"
echo ""
echo "Student Account:"
echo "  Email: demo.student@collabio.com"
echo "  Password: (any password works)"
echo ""
echo "Employer Account:"
echo "  Email: demo.employer@techcorp.com"
echo "  Password: (any password works)"
echo ""
echo "======================================"
echo ""
echo "Starting server..."
echo ""

# Start the development server
npm run dev
