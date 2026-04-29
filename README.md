# Security Analysis Agent

This agent analyzes security threats in APIs and container images, including base images, and generates comprehensive reports with risks and resolutions.

## Features

- API Security Analysis: Checks for common vulnerabilities like missing headers, sensitive data exposure.
- Image Vulnerability Scanning: Uses Trivy to scan container images for known vulnerabilities.
- Report Generation: Produces detailed reports with identified risks and suggested resolutions.

## Installation

1. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Install Trivy for image scanning:
   ```
   # On macOS
   brew install trivy
   ```
   If Homebrew is not available, install the local project copy:
   ```
   sh install_trivy.sh
   ```

## Usage

Run the agent:

```python
from src.security_agent.main import SecurityAgent

agent = SecurityAgent()
api_report = agent.analyze_api('https://example.com/api/endpoint')
image_report = agent.analyze_image('nginx:latest')
report = agent.generate_report([api_report], [image_report])
print(report)
```

## Requirements

- Python 3.8+
- Trivy (for image scanning)
- Internet connection for API testing
