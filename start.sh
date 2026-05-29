#!/bin/bash
# CyberShield startup script

echo "🚀 Starting CyberShield Security Operations Platform..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

# Initialize database if needed
if [ ! -f "cybershield.db" ]; then
    echo "🗄️  Initializing database..."
    python3 << EOF
from app import create_app
app = create_app()
with app.app_context():
    from src.models import db
    db.create_all()
print("✅ Database initialized successfully!")
EOF
fi

# Check for Trivy
if ! command -v trivy &> /dev/null; then
    echo "⚠️  Trivy not found. Installing..."
    if command -v brew &> /dev/null; then
        brew install trivy
    else
        echo "Please install Trivy manually: https://aquasecurity.github.io/trivy/latest/getting-started/installation/"
        echo "Or run: sh install_trivy.sh"
    fi
fi

# Display startup information
echo ""
echo "================================================"
echo "✅ CyberShield is Ready to Start!"
echo "================================================"
echo ""
echo "🌐 Access the platform at: http://localhost:5000"
echo ""
echo "📝 Default credentials (after creating account):"
echo "   - Visit http://localhost:5000 to register"
echo ""
echo "🤖 CyberGuard AI Bot features:"
echo "   ✓ Security requirement analysis"
echo "   ✓ API vulnerability scanning"
echo "   ✓ Container image analysis"
echo "   ✓ Compliance recommendations"
echo ""
echo "Starting Flask server..."
echo ""

# Start the application
python3 app.py
