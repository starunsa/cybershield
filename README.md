# CyberShield - Production Grade Security Operations Platform

A comprehensive, production-ready security operations platform with intelligent chatbot, multi-user authentication, and enterprise-grade security analysis capabilities.

## 🚀 Features

### Core Platform
- **Multi-User Authentication**: Secure JWT-based authentication system
- **User Management**: User registration, login, profile management, and password change
- **Database Persistence**: SQLite database for user sessions and chat history
- **Production Ready**: Proper error handling, logging, and security measures

### Intelligent Chatbot (CyberGuard)
- **Smart Requirement Understanding**: NLP-based intent detection for security requirements
- **Conversational Interface**: Interactive chat that understands user security needs
- **Context-Aware Responses**: Provides tailored guidance based on identified intents
- **Session Management**: Maintains chat history across sessions
- **Personalized Greetings**: Shows bot name and logged-in user information

### Security Analysis
- **API Security Analysis**: Analyzes REST APIs for vulnerabilities and security risks
- **Container Image Scanning**: Scans Docker/OCI images for vulnerabilities using Trivy
- **Report Generation**: Creates comprehensive security reports combining multiple analyses
- **Risk Assessment**: Identifies and categorizes security risks

### User Interface
- **Responsive Dashboard**: Modern, professional web interface
- **Chat Widget**: Real-time chat interface with CyberGuard AI
- **Security Console**: Dedicated sections for API analysis and image scanning
- **User Profile Management**: Update profile and change passwords
- **Session History**: Access previous chat sessions and analysis results

## 📋 Requirements

- Python 3.8 or higher
- Trivy (for container image scanning)
- Modern web browser

## 🔧 Installation

### 1. Clone/Setup Project
```bash
cd /path/to/codex
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Trivy
```bash
# macOS
brew install trivy

# Or use the installation script
sh install_trivy.sh

# Linux/Docker - see https://aquasecurity.github.io/trivy/latest/getting-started/installation/
```

### 5. Initialize Database
```bash
python3
>>> from app import create_app
>>> app = create_app()
>>> with app.app_context():
...     from src.models import db
...     db.create_all()
>>> exit()
```

### 6. Configure Environment (Optional)
Copy `.env.example` to `.env` and customize settings for your deployment:
```bash
cp .env.example .env
```

Example values in `.env`:
```env
FLASK_ENV=development
DEBUG=True
PORT=5003
DATABASE_URL=sqlite:///instance/cybershield.db
JWT_SECRET_KEY=change-this-in-production
CORS_ORIGINS=http://localhost:5003
```

## 🚀 Running the Application

### Development Mode
```bash
python3 app.py
```

The application will be available at `http://localhost:5000`

### Production Mode
```bash
export FLASK_ENV=production
export PORT=5000
export JWT_SECRET_KEY=replace-with-secure-random-secret
gunicorn -w 4 -b 0.0.0.0:${PORT} app:create_app()
```

### Docker
Build and run the production container:
```bash
docker build -t cybershield:latest .
docker run -d -p 5000:5000 --env-file .env --name cybershield cybershield:latest
```

## 💻 Using the Application

### First Time Setup
1. **Open the Application**: Navigate to `http://localhost:5000` in your browser
2. **Create Account**: Click "Create Account" and register with your credentials
3. **Login**: Use your credentials to login

### Dashboard Overview
After login, you'll see the main dashboard with:
- **Navigation Bar**: Quick access to all platform features
- **Sidebar**: User profile, recent chats, and quick actions
- **Welcome Banner**: Platform overview and feature highlights

### Interacting with CyberGuard AI

1. **Click "Security Chat"** in the navigation or dashboard
2. **Greeting**: CyberGuard will greet you with the message: 
   ```
   "Hello [Your Username]! 👋 I'm CyberGuard, your AI Security Assistant..."
   ```
3. **Chat**: Describe your security requirements or needs:
   - "I need to analyze my API security"
   - "Scan my Docker image for vulnerabilities"
   - "Help me understand compliance requirements"
4. **Bot Response**: CyberGuard will understand your intent and provide:
   - Relevant guidance and options
   - Security analysis recommendations
   - Next steps for your specific needs

### API Security Analysis
1. Navigate to **"Analysis"** → **"API Analysis"**
2. Enter your API endpoint URL
3. Select HTTP method
4. Click **"Analyze API"** to run the security audit
5. View comprehensive security report

### Container Image Scanning
1. Navigate to **"Analysis"** → **"Image Scanning"**
2. Enter container image name (e.g., `nginx:latest`, `myapp:1.0`)
3. Click **"Scan Image"** to scan for vulnerabilities
4. Review vulnerability details and remediation steps

### Generate Reports
1. Navigate to **"Analysis"** → **"Generate Report"**
2. Enter API URLs and container image names (comma-separated)
3. Click **"Generate Report"** to create comprehensive security documentation
4. Export or download the detailed report

### Profile Management
1. Click your username in the navigation
2. Update full name or email address
3. Change password in the separate section
4. Save changes

## 🏗️ Project Structure

```
codex/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── .env                           # Environment configuration
├── README.md                      # This file
│
├── src/
│   ├── __init__.py
│   ├── models.py                  # Database models (User, ChatSession, ChatMessage)
│   ├── config.py                  # Application configuration
│   ├── auth.py                    # Authentication service & decorators
│   ├── chatbot.py                 # CyberGuard AI chatbot service
│   ├── routes.py                  # API routes and blueprints
│   └── security_agent/
│       ├── __init__.py
│       └── main.py                # Security analysis engine
│
├── templates/
│   ├── login.html                 # Login/Registration page
│   └── dashboard.html             # Main dashboard with chatbot
│
├── static/
│   ├── css/
│   │   ├── style.css              # Base styles and authentication
│   │   └── dashboard.css          # Dashboard layout and styling
│   └── js/
│       ├── auth.js                # Authentication logic
│       └── dashboard.js           # Dashboard and chat functionality
│
└── tests/                         # Test files (expandable)
```

## 🔐 Security Features

- **JWT Authentication**: Stateless token-based authentication
- **Password Hashing**: PBKDF2 with SHA256 for password security
- **CORS Protection**: Configured CORS with allowed origins
- **Session Security**: Secure session cookies with HttpOnly flag
- **Input Validation**: All inputs validated and sanitized
- **Error Handling**: Comprehensive error handling with user-friendly messages

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/validate` - Validate token (requires auth)

### Chat
- `POST /api/chat/greeting` - Get bot greeting (requires auth)
- `POST /api/chat/send` - Send message to chatbot (requires auth)
- `GET /api/chat/history/<session_id>` - Get chat history (requires auth)
- `GET /api/chat/sessions` - List user's chat sessions (requires auth)

### Security Analysis
- `POST /api/security/analyze-api` - Analyze API (requires auth)
- `POST /api/security/scan-image` - Scan container image (requires auth)
- `POST /api/security/report` - Generate security report (requires auth)

### User
- `GET /api/user/profile` - Get user profile (requires auth)
- `PUT /api/user/profile` - Update profile (requires auth)
- `POST /api/user/change-password` - Change password (requires auth)

## 🧪 Testing

To test authentication:
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"test123","full_name":"Test User"}'

curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"test123"}'
```

## 🐛 Troubleshooting

### Database Issues
```bash
# Reset database
rm cybershield.db
python3 app.py
```

### Port Already in Use
```bash
# Use different port
PORT=5001 python3 app.py
```

### Module Import Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

### Trivy Not Found
```bash
# Install Trivy
brew install trivy

# Or specify path in environment
export TRIVY_PATH=/path/to/trivy
```

## 📊 CyberGuard AI Capabilities

CyberGuard understands and responds to queries about:

1. **Security Analysis** - API and container scanning
2. **API Security** - Endpoint vulnerabilities and headers
3. **Image Scanning** - Container vulnerability detection
4. **Compliance** - GDPR, HIPAA, PCI-DSS, SOC2
5. **Vulnerabilities** - CVE identification and remediation
6. **General Guidance** - Security best practices

## 🚀 Performance & Scalability

- **Efficient Database**: SQLAlchemy ORM with proper indexing
- **Async Operations**: Non-blocking I/O for responsive UI
- **Caching**: Chat history cached on client side
- **Horizontal Scaling**: Stateless Flask app design
- **Load Balancing**: Ready for nginx/Apache deployment

## 📝 Future Enhancements

- [ ] Multi-language support
- [ ] Advanced reporting with PDF export
- [ ] Real-time notifications
- [ ] Team collaboration features
- [ ] Integration with SIEM platforms
- [ ] Machine learning-based risk scoring
- [ ] GraphQL API support

## 📄 License

Proprietary - CyberShield Security Operations Platform

## 👨‍💼 Support

For issues or questions, contact the security team.

## 🙏 Credits

- Built with Flask, SQLAlchemy, and modern web technologies
- Security analysis powered by Trivy and custom security modules
- UI designed for modern browsers and responsive devices

