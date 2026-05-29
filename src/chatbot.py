"""
Chatbot Service - Intelligent conversation handler
"""
from typing import Dict, List, Optional
from datetime import datetime
import re

class ChatbotService:
    """
    Intelligent chatbot for security consultations and requirements analysis
    """
    
    BOT_NAME = "CyberGuard"
    
    # Intent patterns for understanding user requirements
    INTENT_PATTERNS = {
        'security_analysis': [r'analyze|scan|check|test', r'security|vulnerability|threat'],
        'compliance': [r'compliance|gdpr|hipaa|pci|soc2', r'compliance|standard|regulation'],
        'vulnerability': [r'vulnerability|cve|exploit|weakness'],
        'api_security': [r'api|endpoint|rest|graphql', r'security|vulnerable|risk'],
        'image_scanning': [r'image|container|docker', r'scan|vulnerability|threat'],
        'report': [r'report|generate|create', r'security|analysis|vulnerability'],
    }
    
    def __init__(self):
        self.bot_name = self.BOT_NAME
        self.conversation_history: List[Dict] = []
    
    def get_greeting(self, username: str) -> str:
        """Generate welcome greeting"""
        greeting = f"Hello {username}! 👋 I'm {self.bot_name}, your AI Security Assistant. "
        greeting += "I can help you with API security analysis, container image scanning, "
        greeting += "compliance checks, and security threat assessments. What can I help you with today?"
        return greeting
    
    def understand_requirement(self, user_input: str) -> Dict:
        """Analyze user input to understand requirements"""
        user_input_lower = user_input.lower()
        
        identified_intents = []
        for intent, patterns in self.INTENT_PATTERNS.items():
            # Check if all patterns match
            if all(re.search(pattern, user_input_lower) for pattern in patterns):
                identified_intents.append(intent)
        
        return {
            'input': user_input,
            'intents': identified_intents,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def generate_response(self, user_message: str, username: str) -> str:
        """Generate contextual bot response"""
        analysis = self.understand_requirement(user_message)
        intents = analysis['intents']
        
        # Route based on identified intents
        if 'security_analysis' in intents:
            return self._handle_security_analysis(user_message, username)
        elif 'api_security' in intents:
            return self._handle_api_security(user_message, username)
        elif 'image_scanning' in intents:
            return self._handle_image_scanning(user_message, username)
        elif 'compliance' in intents:
            return self._handle_compliance(user_message, username)
        elif 'vulnerability' in intents:
            return self._handle_vulnerability(user_message, username)
        else:
            return self._handle_general_query(user_message, username)
    
    def _handle_security_analysis(self, user_input: str, username: str) -> str:
        return (
            f"Great! {username}, I'll help you with a comprehensive security analysis. "
            f"\n\n📊 **Security Analysis Options:**\n"
            f"1. **API Security Audit** - Check your API endpoints for vulnerabilities\n"
            f"2. **Container Image Scan** - Scan Docker/container images for threats\n"
            f"3. **Risk Assessment** - Identify and prioritize security risks\n"
            f"4. **Report Generation** - Create detailed security reports\n\n"
            f"Please provide the target URL or image name you'd like me to analyze."
        )
    
    def _handle_api_security(self, user_input: str, username: str) -> str:
        return (
            f"Perfect! {username}, I'll conduct an API security review. "
            f"\n\n🔍 **API Security Checks:**\n"
            f"✓ Authentication & Authorization\n"
            f"✓ Input Validation\n"
            f"✓ Data Exposure\n"
            f"✓ Security Headers\n"
            f"✓ Rate Limiting\n"
            f"✓ CORS Configuration\n\n"
            f"Please provide the API endpoint URL you'd like me to test."
        )
    
    def _handle_image_scanning(self, user_input: str, username: str) -> str:
        return (
            f"Excellent! {username}, I'll scan your container image for vulnerabilities. "
            f"\n\n🐳 **Image Scanning will check:**\n"
            f"• Known CVEs (Common Vulnerabilities and Exposures)\n"
            f"• Base image vulnerabilities\n"
            f"• Dependency vulnerabilities\n"
            f"• Configuration issues\n\n"
            f"Please provide the container image name (e.g., 'nginx:latest' or 'myapp:1.0')."
        )
    
    def _handle_compliance(self, user_input: str, username: str) -> str:
        return (
            f"Great question, {username}! I can help with compliance requirements. "
            f"\n\n📋 **Compliance Frameworks Supported:**\n"
            f"• GDPR (General Data Protection Regulation)\n"
            f"• HIPAA (Healthcare)\n"
            f"• PCI-DSS (Payment Card Industry)\n"
            f"• SOC 2 (Service Organization Control)\n"
            f"• ISO 27001 (Information Security)\n\n"
            f"Which framework are you targeting, or would you like a multi-framework assessment?"
        )
    
    def _handle_vulnerability(self, user_input: str, username: str) -> str:
        return (
            f"I'll help you identify vulnerabilities, {username}. "
            f"\n\n🚨 **Vulnerability Assessment includes:**\n"
            f"• CVE Database Lookup\n"
            f"• Risk Severity Classification\n"
            f"• Remediation Steps\n"
            f"• Patch Recommendations\n\n"
            f"What would you like to scan for vulnerabilities? (API endpoint or container image)"
        )
    
    def _handle_general_query(self, user_input: str, username: str) -> str:
        return (
            f"Thanks for reaching out, {username}! I can assist with:\n\n"
            f"🔒 **Security Analysis** - API and container scanning\n"
            f"📊 **Risk Assessment** - Identify security threats\n"
            f"📋 **Compliance Checks** - GDPR, HIPAA, PCI-DSS, SOC 2\n"
            f"🐳 **Container Security** - Docker image vulnerability scanning\n"
            f"📈 **Reports** - Comprehensive security documentation\n\n"
            f"What would you like to focus on today?"
        )
    
    def process_chat(self, user_message: str, username: str) -> Dict:
        """Process user message and generate bot response"""
        bot_response = self.generate_response(user_message, username)
        
        return {
            'user_message': user_message,
            'bot_response': bot_response,
            'bot_name': self.bot_name,
            'username': username,
            'timestamp': datetime.utcnow().isoformat()
        }
