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
        'website_scanning': [r'website|site|web app|url|domain', r'scan|check|test|suggest|recommend|name'],
        'report': [r'report|generate|create', r'security|analysis|vulnerability'],
    }
    
    def __init__(self):
        self.bot_name = self.BOT_NAME
        self.conversation_history: List[Dict] = []
    
    def get_greeting(self, username: str) -> str:
        """Generate welcome greeting"""
        return (
            f"Welcome back, {username}. I'm {self.bot_name}, your CyberShield assistant.\n\n"
            "I can help you choose the right scan, explain findings, and generate a security report.\n\n"
            "Try one of these:\n"
            "- Scan a website for HTTPS and security headers\n"
            "- Review an API endpoint for common risks\n"
            "- Check a container image for vulnerabilities\n"
            "- Build a combined report for your audit notes"
        )
    
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

        if self._looks_like_container_image(user_message):
            return self._handle_image_scanning(user_message, username)

        if self._looks_like_url(user_message):
            return self._handle_website_scanning(user_message, username)

        if self._mentions_image_asset(user_message) and self._asks_for_examples(user_message):
            return self._handle_image_scanning(user_message, username)

        if self._mentions_website_asset(user_message) and self._asks_for_examples(user_message):
            return self._handle_website_scanning(user_message, username)

        if self._mentions_api_asset(user_message) and self._asks_for_examples(user_message):
            return self._handle_api_security(user_message, username)
        
        # Route based on identified intents
        if 'website_scanning' in intents:
            return self._handle_website_scanning(user_message, username)
        elif 'api_security' in intents:
            return self._handle_api_security(user_message, username)
        elif 'image_scanning' in intents:
            return self._handle_image_scanning(user_message, username)
        elif 'security_analysis' in intents:
            return self._handle_security_analysis(user_message, username)
        elif 'compliance' in intents:
            return self._handle_compliance(user_message, username)
        elif 'vulnerability' in intents:
            return self._handle_vulnerability(user_message, username)
        else:
            return self._handle_general_query(user_message, username)

    def _asks_for_examples(self, user_input: str) -> bool:
        user_input_lower = user_input.lower()
        return bool(re.search(r'\b(give|suggest|recommend|example|sample|which|what|name|list|show)\b', user_input_lower))

    def _looks_like_container_image(self, user_input: str) -> bool:
        return bool(re.search(r'\b[a-z0-9][a-z0-9._/-]+:[a-z0-9._-]+\b', user_input.lower()))

    def _looks_like_url(self, user_input: str) -> bool:
        return bool(re.search(r'https?://|www\.|[a-z0-9-]+\.[a-z]{2,}', user_input.lower()))

    def _mentions_image_asset(self, user_input: str) -> bool:
        return bool(re.search(r'\b(image|container|docker)\b', user_input.lower()))

    def _mentions_website_asset(self, user_input: str) -> bool:
        return bool(re.search(r'\b(website|site|web app|url|domain)\b', user_input.lower()))

    def _mentions_api_asset(self, user_input: str) -> bool:
        return bool(re.search(r'\b(api|endpoint|rest|graphql)\b', user_input.lower()))
    
    def _handle_security_analysis(self, user_input: str, username: str) -> str:
        return (
            f"Great, {username}. I can guide a complete security check.\n\n"
            "Available scans:\n"
            "1. API Security Audit - endpoints, headers, exposure, and auth posture\n"
            "2. Website Scan - HTTPS, security headers, and common web risks\n"
            "3. Container Image Scan - known vulnerabilities and package risk\n"
            "4. Report Generation - one combined summary for review or audit\n\n"
            "Send me a URL, API endpoint, or image name and I will point you to the right scanner."
        )
    
    def _handle_api_security(self, user_input: str, username: str) -> str:
        if self._asks_for_examples(user_input):
            return (
                f"Here are safe API endpoints you can use for a quick test, {username}:\n\n"
                "- https://httpbin.org/get\n"
                "- https://jsonplaceholder.typicode.com/posts/1\n"
                "- Any API endpoint from your own staging app\n\n"
                "Open Analysis > API Analysis, paste one endpoint, choose GET, and run the scan."
            )

        if self._looks_like_url(user_input):
            return (
                f"That looks like an API or web URL, {username}.\n\n"
                "If it is an API endpoint, open Analysis > API Analysis and paste it there.\n"
                "If it is a regular website, use Analysis > Website Scanning instead.\n\n"
                "Tip: API targets usually look like /api, /v1, /graphql, or return JSON."
            )

        return (
            f"Perfect, {username}. For an API security review, I will look for:\n\n"
            "- Authentication and authorization gaps\n"
            "- Missing security headers\n"
            "- Sensitive data exposure\n"
            "- CORS and method configuration issues\n"
            "- Basic response and availability signals\n\n"
            "Paste the API endpoint URL when you are ready."
        )
    
    def _handle_image_scanning(self, user_input: str, username: str) -> str:
        if self._looks_like_container_image(user_input):
            return (
                f"That looks like a valid container image target, {username}.\n\n"
                "Open Analysis > Image Scanning and paste it exactly as written.\n\n"
                "After the scan, focus first on CRITICAL and HIGH findings, then update the base image or affected packages."
            )

        if self._asks_for_examples(user_input):
            return (
                f"Sure, {username}. Try one of these container images for a scan:\n\n"
                "- nginx:latest\n"
                "- alpine:latest\n"
                "- python:3.11-slim\n"
                "- node:20-alpine\n\n"
                "For the fastest demo, use alpine:latest. For a more realistic web-server example, use nginx:latest."
            )

        return (
            f"Excellent, {username}. Container image scanning checks:\n\n"
            "- Known CVEs in OS packages and dependencies\n"
            "- Base image risk\n"
            "- High and critical vulnerability counts\n"
            "- Suggested fixed package versions when available\n\n"
            "Send an image name such as nginx:latest or your private image tag."
        )

    def _handle_website_scanning(self, user_input: str, username: str) -> str:
        if self._looks_like_url(user_input):
            return (
                f"That looks like a website target, {username}.\n\n"
                "Open Analysis > Website Scanning, paste the URL, and run the scan.\n\n"
                "CyberShield will check HTTPS, security headers, XSS guidance, SQL injection guidance, CSRF posture, and an overall score."
            )

        if self._asks_for_examples(user_input):
            return (
                f"Here are safe website examples you can scan, {username}:\n\n"
                "- https://example.com\n"
                "- https://owasp.org\n"
                "- https://httpbin.org\n"
                "- A staging URL that belongs to your project\n\n"
                "I recommend starting with https://example.com because it is stable and quick."
            )

        return (
            f"Good choice, {username}. Website scanning is best for checking public web pages, staging apps, or internal URLs you own.\n\n"
            "Good safe examples to try:\n"
            "- https://example.com\n"
            "- https://owasp.org\n"
            "- Your own staging or production website URL\n\n"
            "The scan will review HTTPS, key security headers, XSS guidance, SQL injection guidance, CSRF posture, and an overall score."
        )
    
    def _handle_compliance(self, user_input: str, username: str) -> str:
        return (
            f"Great question, {username}. I can help map scan findings to compliance themes.\n\n"
            "Frameworks I can help reason about:\n"
            "- GDPR\n"
            "- HIPAA\n"
            "- PCI-DSS\n"
            "- SOC 2\n"
            "- ISO 27001\n\n"
            "Tell me which framework you are targeting and what asset you want to assess."
        )
    
    def _handle_vulnerability(self, user_input: str, username: str) -> str:
        return (
            f"I can help you identify and prioritize vulnerabilities, {username}.\n\n"
            "A useful assessment usually includes:\n"
            "- Asset type: website, API, or container image\n"
            "- Severity classification\n"
            "- Remediation guidance\n"
            "- Report notes for tracking\n\n"
            "Send the target you want to scan."
        )
    
    def _handle_general_query(self, user_input: str, username: str) -> str:
        return (
            f"I'm here, {username}. Tell me what you want to protect and I will help choose the right scan.\n\n"
            "I can help with:\n"
            "- Website scanning: HTTPS, headers, and web risk posture\n"
            "- API security: endpoint checks and exposure review\n"
            "- Container security: image vulnerability scanning\n"
            "- Compliance support: GDPR, HIPAA, PCI-DSS, SOC 2\n"
            "- Reports: combined findings and remediation notes\n\n"
            "For a quick start, try: suggest a website I can scan."
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
