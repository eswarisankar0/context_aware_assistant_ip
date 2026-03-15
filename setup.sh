#!/bin/bash

echo "🚀 Setting up Context-Aware Assistant Project"
echo "============================================"

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file template..."
    cat > .env << EOF
# Add your Anthropic API key here
ANTHROPIC_API_KEY=your_api_key_here
EOF
    echo "✅ .env file created. Please edit it and add your Anthropic API key."
    echo "   Get your API key from: https://console.anthropic.com/"
else
    echo "✅ .env file already exists"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd reminder-dashboard
npm install
cd ..

echo ""
echo "🎯 Setup complete!"
echo ""
echo "To run the project:"
echo "1. Edit .env file and add your Anthropic API key"
echo "2. Run the backend API: uvicorn app.api:app --reload --port 8000"
echo "3. Run the frontend: cd reminder-dashboard && npm run dev"
echo "4. Or run the CLI: python main.py"
echo ""
echo "The project will be available at:"
echo "- Backend API: http://localhost:8000"
echo "- Frontend: http://localhost:5173"
