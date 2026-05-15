##### Security Analysis Agent

This agent analyzes security threats in APIs and container images, including base images, and generates comprehensive reports with risks and resolutions.

## Features

- **API Security Analysis**: Checks for common vulnerabilities like missing headers, sensitive data exposure.
- **Image Vulnerability Scanning**: Uses Trivy to scan container images for known vulnerabilities.
- **Report Generation**: Produces detailed reports with identified risks and suggested resolutions.

## Installation

### Prerequisites

Before installing CyberShield, ensure you have the following installed on your system:

- **Python 3.8 or higher** ([Download Python](https://www.python.org/downloads/))
- **pip** (usually comes with Python)
- **git** (for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/starunsa/cybershield.git
cd cybershield
```

### Step 2: Install Python Dependencies

Install all required Python packages using the requirements file:

```bash
pip install -r requirements.txt
```

Or, if you're using Python 3 specifically:

```bash
pip3 install -r requirements.txt
```

### Step 3: Install Trivy for Image Scanning

Trivy is required for container image vulnerability scanning. Choose the installation method that works best for your system:

#### Option A: Using Homebrew (macOS/Linux)

```bash
brew install trivy
```

#### Option B: Using the Installation Script

If Homebrew is not available or you prefer an automated setup:

```bash
sh install_trivy.sh
```

#### Option C: Manual Installation

Visit the [Trivy GitHub Releases](https://github.com/aquasecurity/trivy/releases) page to download and install manually for your operating system.

### Step 4: Verify Installation

Verify that everything is installed correctly:

```bash
# Check Python version
python --version

# Check pip
pip --version

# Check Trivy
trivy version
```

## Usage

Run the agent with the following example:

```python
from src.security_agent.main import SecurityAgent

agent = SecurityAgent()
api_report = agent.analyze_api('https://example.com/api/endpoint')
image_report = agent.analyze_image('nginx:latest')
report = agent.generate_report([api_report], [image_report])
print(report)
```

## Requirements

- **Python 3.8+**
- **Trivy** (for container image scanning)
- **Internet connection** (for API testing and vulnerability databases)
