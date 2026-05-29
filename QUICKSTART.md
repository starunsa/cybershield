#!/bin/bash
# Quick start guide for CyberShield

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  CyberShield - Security Operations Platform               ║"
echo "║  Quick Start Guide                                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "📋 STEP-BY-STEP SETUP:"
echo ""

echo "1️⃣  Install Python Dependencies"
echo "   $ python3 -m venv venv"
echo "   $ source venv/bin/activate"
echo "   $ pip install -r requirements.txt"
echo ""

echo "2️⃣  Install Trivy (for image scanning)"
echo "   $ brew install trivy          # macOS"
echo "   $ sh install_trivy.sh         # Manual installation"
echo ""

echo "3️⃣  Start the Application"
echo "   $ python3 app.py"
echo "   OR"
echo "   $ bash start.sh               # Automatic setup"
echo ""

echo "4️⃣  Open in Browser"
echo "   🌐 http://localhost:5000"
echo ""

echo "════════════════════════════════════════════════════════════"
echo ""

echo "🎯 QUICK TEST:"
echo ""
echo "1. Create an account at http://localhost:5000"
echo "2. Login with your credentials"
echo "3. Click 'Security Chat' in the dashboard"
echo "4. Chat with CyberGuard AI - try:"
echo "   • 'Analyze my API security'"
echo "   • 'Scan my Docker image'"
echo "   • 'Help with GDPR compliance'"
echo ""

echo "════════════════════════════════════════════════════════════"
echo ""

echo "📚 DOCUMENTATION:"
echo "   • See README.md for full documentation"
echo "   • API endpoints: Check src/routes.py"
echo "   • Database models: Check src/models.py"
echo "   • Chatbot logic: Check src/chatbot.py"
echo ""

echo "🆘 TROUBLESHOOTING:"
echo ""
echo "Q: Port 5000 already in use?"
echo "A: $ PORT=5001 python3 app.py"
echo ""
echo "Q: Trivy not found?"
echo "A: $ brew install trivy"
echo ""
echo "Q: Database error?"
echo "A: $ rm cybershield.db && python3 app.py"
echo ""

echo "════════════════════════════════════════════════════════════"
echo ""
echo "✅ Ready? Start with: python3 app.py"
echo ""
