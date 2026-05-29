"""
Production deployment configuration example
"""

# For Gunicorn deployment
# Install: pip install gunicorn
# Run: gunicorn -w 4 -b 0.0.0.0:5000 --log-level info app:create_app()

# For Docker deployment
# Build: docker build -t cybershield .
# Run: docker run -p 5000:5000 -e FLASK_ENV=production cybershield

# For systemd service on Linux
# /etc/systemd/system/cybershield.service:
"""
[Unit]
Description=CyberShield Security Platform
After=network.target

[Service]
Type=notify
User=cybershield
WorkingDirectory=/opt/cybershield
Environment="PATH=/opt/cybershield/venv/bin"
ExecStart=/opt/cybershield/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
